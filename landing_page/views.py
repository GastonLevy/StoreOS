from django.shortcuts import render
from django_user_agents.utils import get_user_agent

def landing_page(request):
    """
    Render the landing page with a template optimized for the user's device type.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered landing page template for mobile or desktop.

    Raises:
        None explicitly.
    """
    user_agent = get_user_agent(request)
    
    # Render mobile template if device is mobile, otherwise desktop template
    if user_agent.is_mobile:
        return render(request, 'landing_page_mobile.html')
    else:
        return render(request, 'landing_page_desktop.html')
