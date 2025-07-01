from django.shortcuts import render
from django.core.paginator import Paginator
from storeos.decorators import role_required
from ..models import Device

@role_required('Cyber_Admin', 'Cyber')
def device_list(request):
    """
    Lists devices of the user's company with optional search and pagination.

    Args:
        request (HttpRequest): Request object containing optional query parameters:
            - 'search' (str): Search string to filter devices by name (case-insensitive).
            - 'entries' (int): Number of devices per page (default 10, max 100).
            - 'page' (int): Page number for pagination.

    Returns:
        HttpResponse: Rendered page with paginated and optionally filtered devices.

    Raises:
        None explicitly.
    """
    user_profile = request.user.userprofile
    # Get all devices for the user's company
    devices = Device.objects.filter(company=user_profile.company)

    # Get search query string from request (default empty)
    search_query = request.GET.get('search', '').strip()

    if search_query:
        # Filter devices by name case-insensitive if search string is present
        devices = devices.filter(name__icontains=search_query)

    # Get number of entries per page, default 10
    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)
    except ValueError:
        entries_per_page = 10

    # Limit entries_per_page to a reasonable range (1-100)
    if entries_per_page < 1:
        entries_per_page = 10
    elif entries_per_page > 100:
        entries_per_page = 100

    # Setup paginator with filtered devices and entries per page
    paginator = Paginator(devices, entries_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return rendered view with paginated devices and pagination info
    return render(request, 'list_device.html', {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'search_query': search_query
    })
