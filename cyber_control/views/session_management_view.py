from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from storeos.decorators import role_required
from ..models import Device, UsageSession
from django.utils.timezone import now, timedelta, make_aware
from accounts.models import Person
import datetime

@role_required('Cyber_Admin', 'Cyber')
def get_all_remaining_times(request):
    """
    Returns remaining usage time in seconds for all devices of the user's company.

    Args:
        request (HttpRequest): HTTP request, optionally with 'current_time' as a timestamp query param.

    Returns:
        JsonResponse: Dictionary with device IDs, names, client IDs, and remaining time in seconds.

    Raises:
        None explicitly, but database access or timestamp conversion might raise exceptions.
    """
    devices = Device.objects.filter(company=request.user.userprofile.company)
    
    current_time = request.GET.get('current_time')
    if current_time:
        current_time = int(current_time)
    else:
        current_time = int(now().timestamp())

    device_times = []

    for device in devices:
        session = UsageSession.objects.filter(device=device, is_active=True).last()
        if session:
            current_time_aware = make_aware(datetime.datetime.fromtimestamp(current_time))
            remaining_time = session.end_time - current_time_aware
            remaining_seconds = int(remaining_time.total_seconds()) if remaining_time.total_seconds() > 0 else 0

            device_times.append({
                'device_id': device.id,
                'remaining_time_seconds': remaining_seconds,
                'device_name': device.name,
                'client_id': session.client.id if session.client else None
            })
        else:
            device_times.append({
                'device_id': device.id,
                'remaining_time_seconds': 0,
                'device_name': device.name,
                'client_id': None
            })
    
    return JsonResponse({'device_times': device_times})

@role_required('Cyber_Admin', 'Cyber')
def usage_session_list(request):
    """
    Displays a list of devices with their active usage sessions and remaining time.

    Args:
        request (HttpRequest): HTTP request, optionally with 'current_time' timestamp param.

    Returns:
        HttpResponse: Rendered HTML page with devices and clients data.

    Raises:
        None explicitly.
    """
    devices = Device.objects.filter(company=request.user.userprofile.company)
    clients = Person.objects.filter(company=request.user.userprofile.company)

    current_time = request.GET.get('current_time')
    if current_time:
        current_time = int(current_time)
    else:
        current_time = int(now().timestamp())

    for device in devices:
        session = UsageSession.objects.filter(device=device, is_active=True).last()
        if session:
            current_time_aware = make_aware(datetime.datetime.fromtimestamp(current_time))
            remaining_time = session.end_time - current_time_aware
            device.remaining_time_seconds = int(remaining_time.total_seconds()) if remaining_time.total_seconds() > 0 else 0
            device.session_active = True
            device.client = session.client
        else:
            device.remaining_time_seconds = 0
            device.session_active = False
            device.client = None
        device.save()

    return render(request, 'usage_session_list.html', {
        'devices': devices,
        'clients': clients
    })

def end_session(request, device_id):
    """
    Ends the active usage session for a given device.

    Args:
        request (HttpRequest): HTTP request, can be AJAX or normal.
        device_id (int): The ID of the device.

    Returns:
        JsonResponse if AJAX: success message.
        HttpResponseRedirect otherwise: redirects to 'device_list'.

    Raises:
        None explicitly.
    """
    usage_session = UsageSession.objects.filter(device_id=device_id, is_active=True).last()
    
    if usage_session:
        usage_session.is_active = False
        usage_session.save()
    
    if request.is_ajax():
        return JsonResponse({'success': True, 'message': 'Sesión terminada'})

    return redirect('device_list')

@role_required('Cyber_Admin', 'Cyber')
def add_usage_time(request, device_id):
    """
    Adds usage time to an active session or creates a new session for a device.

    Args:
        request (HttpRequest): POST request with 'duration' (minutes), 'current_time' (timestamp), and optional 'client_id'.
        device_id (int): The ID of the device to add time to.

    Returns:
        JsonResponse: Success with remaining seconds or error message.

    Raises:
        JsonResponse with status 400 for invalid duration.
        JsonResponse with status 404 if client not found.
        JsonResponse with status 405 if method not allowed.
    """
    if request.method == 'POST':
        device = get_object_or_404(Device, id=device_id, company=request.user.userprofile.company)
        duration_minutes = int(request.POST.get('duration', 0))
        current_time = int(request.POST.get('current_time', 0))
        client_id = request.POST.get('client_id')

        if duration_minutes <= 0:
            return JsonResponse({'error': 'Duración inválida.'}, status=400)

        current_time_aware = make_aware(datetime.datetime.fromtimestamp(current_time))
        session = UsageSession.objects.filter(device=device, is_active=True).last()

        if not session or session.end_time <= current_time_aware:
            new_end_time = current_time_aware + timedelta(minutes=duration_minutes)
            session = UsageSession.objects.create(
                device=device,
                client=None,
                company=request.user.userprofile.company,
                start_time=current_time_aware,
                duration=timedelta(minutes=duration_minutes),
                total_duration=timedelta(minutes=duration_minutes),
                end_time=new_end_time
            )
        else:
            new_end_time = session.end_time + timedelta(minutes=duration_minutes)
            session.total_duration += timedelta(minutes=duration_minutes)
            session.end_time = new_end_time
            session.save()

        if client_id:
            try:
                client = Person.objects.get(id=client_id, company=request.user.userprofile.company)
                session.client = client
                session.save()
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Cliente no encontrado.'}, status=404)

        remaining_time = max(new_end_time - current_time_aware, timedelta(0))
        return JsonResponse({
            'success': 'Tiempo agregado exitosamente.',
            'remaining_seconds': int(remaining_time.total_seconds())
        })

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
