from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from storeos.decorators import role_required
from ..models import UsageSession

from django.core.paginator import Paginator

@role_required('Cyber_Admin', 'Cyber')
def usage_reports(request):
    """
    Generates usage reports for the company related to client and device usage.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with usage report context.

    Raises:
        None explicitly, but database queries may raise exceptions.
    """
    user_profile = request.user.userprofile
    company = user_profile.company

    # Date 30 days ago
    thirty_days_ago = now() - timedelta(days=30)

    # Total hours by registered clients (all time)
    registered_hours = UsageSession.objects.filter(company=company, client__isnull=False).aggregate(
        total_hours=Sum('total_duration')
    )['total_hours']

    # Total hours by unregistered clients (all time)
    unregistered_hours = UsageSession.objects.filter(company=company, client__isnull=True).aggregate(
        total_hours=Sum('total_duration')
    )['total_hours']

    # Total hours by registered clients (last 30 days)
    registered_hours_30_days = UsageSession.objects.filter(company=company, client__isnull=False, start_time__gte=thirty_days_ago).aggregate(
        total_hours=Sum('total_duration')
    )['total_hours']

    # Total hours by unregistered clients (last 30 days)
    unregistered_hours_30_days = UsageSession.objects.filter(company=company, client__isnull=True, start_time__gte=thirty_days_ago).aggregate(
        total_hours=Sum('total_duration')
    )['total_hours']

    # Pagination for top clients (last 30 days)
    top_clients_30_days = (
        UsageSession.objects.filter(company=company, start_time__gte=thirty_days_ago, client__isnull=False)
        .values('client__id', 'client__first_name', 'client__last_name')
        .annotate(total_hours=Sum('total_duration'))
        .order_by('-total_hours')
    )
    paginator_clients_30 = Paginator(top_clients_30_days, 10)  # 10 per page
    page_clients_30 = request.GET.get('page_clients_30')
    clients_page_obj = paginator_clients_30.get_page(page_clients_30)

    # Pagination for top devices (last 30 days)
    top_devices_30_days = (
        UsageSession.objects.filter(company=company, start_time__gte=thirty_days_ago)
        .values('device__id', 'device__name')
        .annotate(total_hours=Sum('total_duration'))
        .order_by('-total_hours')
    )
    paginator_devices_30 = Paginator(top_devices_30_days, 10)  # 10 per page
    page_devices_30 = request.GET.get('page_devices_30')
    devices_page_obj = paginator_devices_30.get_page(page_devices_30)

    # Pagination for top clients (all time)
    top_clients = (
        UsageSession.objects.filter(company=company, client__isnull=False)
        .values('client__id', 'client__first_name', 'client__last_name')
        .annotate(total_hours=Sum('total_duration'))
        .order_by('-total_hours')
    )
    paginator_clients = Paginator(top_clients, 10)  # 10 per page
    page_clients = request.GET.get('page_clients')
    clients_page_obj_all = paginator_clients.get_page(page_clients)

    # Pagination for top devices (all time)
    top_devices = (
        UsageSession.objects.filter(company=company)
        .values('device__id', 'device__name')
        .annotate(total_hours=Sum('total_duration'))
        .order_by('-total_hours')
    )
    paginator_devices = Paginator(top_devices, 10)  # 10 per page
    page_devices = request.GET.get('page_devices')
    devices_page_obj_all = paginator_devices.get_page(page_devices)

    return render(request, 'usage_reports.html', {
        'registered_hours': registered_hours,
        'unregistered_hours': unregistered_hours,
        'registered_hours_30_days': registered_hours_30_days,
        'unregistered_hours_30_days': unregistered_hours_30_days,
        'clients_page_obj': clients_page_obj,
        'devices_page_obj': devices_page_obj,
        'clients_page_obj_all': clients_page_obj_all,
        'devices_page_obj_all': devices_page_obj_all,
    })
