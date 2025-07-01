from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from storeos.decorators import role_required
from ..models import Device

@role_required('Cyber_Admin', 'Cyber_Eliminar_Dispositivo')
def device_delete(request, device_id):
    """
    Deletes a device belonging to the user's company after confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        device_id (int): ID of the device to delete.

    Returns:
        HttpResponse: Redirects to device list after deletion on POST,
                        or renders a confirmation page on GET.

    Raises:
        Http404: If the device does not exist or does not belong to the user's company.
        Exception: Any exception during deletion is caught and shown as an error message.
    """
    user_profile = request.user.userprofile
    # Get the device and ensure it belongs to the logged-in user's company
    device = get_object_or_404(Device, id=device_id, company=user_profile.company)
    
    if request.method == 'POST':
        try:
            device_name = device.name
            device.delete()
            messages.success(request, f'Dispositivo "{device_name}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Hubo un problema al eliminar el dispositivo: {str(e)}')
        return redirect('device-list')
    
    # Render the device deletion confirmation page
    return render(request, 'device_confirm_delete.html', {'device': device})
