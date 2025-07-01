from django.shortcuts import render, get_object_or_404, redirect
from ..models import Device
from storeos.decorators import role_required
from ..forms import DeviceForm

@role_required('Cyber_Admin', 'Cyber_Crear_Editar_Dispositivo')
def create_or_edit_device(request, device_id=None):
    """
    Creates a new device or edits an existing one if device_id is provided.

    Args:
        request (HttpRequest): The HTTP request object.
        device_id (int, optional): The ID of the device to edit. Defaults to None.

    Returns:
        HttpResponse: Redirects to the device list on successful save,
                        or renders the form with errors if invalid.
                        Renders the form pre-filled on GET requests.

    Raises:
        Http404: If the device with device_id does not exist.
        PermissionDenied (403): If the device's company does not match the user's company.
    """
    # If device_id is provided, fetch the device for editing
    if device_id:
        device = get_object_or_404(Device, id=device_id)
        
        # Check that the device's company matches the user's company
        if device.company != request.user.userprofile.company:
            return render(request, 'error.html', {'message': 'No tienes permiso para editar este dispositivo.'}, status=403)
    else:
        device = None

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            # Associate the device with the user's company
            company = request.user.userprofile.company
            device = form.save(commit=False)
            device.company = company
            device.save()
            return redirect('device-list')  # Redirect to the device list
        else:
            # Render the form with errors
            return render(request, 'create_or_edit_device.html', {'form': form, 'device': device})

    else:
        # On GET, show the empty form or pre-filled with device data
        form = DeviceForm(instance=device)

    return render(request, 'create_or_edit_device.html', {'form': form, 'device': device})
