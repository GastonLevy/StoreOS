from django.shortcuts import render
from self_wiki.models import WikiCategory

def wiki_overview(request):
    """
    Displays the list of categories along with their preloaded entries to optimize queries.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: Renders the template with categories and their entries.
    """
    categories = WikiCategory.objects.prefetch_related('entries')
    return render(request, 'wiki_user/wiki_overview.html', {'categories': categories})
