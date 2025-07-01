from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from self_logs.models import ActionLog

@login_required
def action_log_list(request):
    """
    Displays a paginated list of system action logs.
    Superusers see all records. Other users see only logs from their company.
    Supports searching by user, action, and details.
    """
    # Check if user is superuser
    if request.user.is_superuser:
        # If superuser, get all logs
        logs = ActionLog.objects.all()
    else:
        # Otherwise, get logs for the user's company
        company = request.user.userprofile.company  # Assuming user profile with company relation exists
        logs = ActionLog.objects.filter(company=company)

    # Get search query term
    search_query = request.GET.get('search', '')

    # If search term exists, filter logs
    if search_query:
        logs = logs.filter(
            Q(action__icontains=search_query) |
            Q(object_id__icontains=search_query) |
            Q(details__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    # Order logs by timestamp descending
    logs = logs.order_by('-timestamp')

    # Pagination
    try:
        entries_per_page = max(1, int(request.GET.get('entries', 25)))  # Default: 25 entries per page, minimum 1
    except ValueError:
        entries_per_page = 25

    paginator = Paginator(logs, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'action_log_list.html',
        {
            'page_obj': page_obj,
            'entries_per_page': entries_per_page
        }
    )
