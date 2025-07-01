from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from self_wiki.models import WikiEntry

def wiki_entry_content(request, entry_id):
    """
    Returns the HTML content of a specific wiki entry.

    Args:
        request (HttpRequest): The HTTP request.
        entry_id (int): ID of the wiki entry.

    Returns:
        HttpResponse: HTTP response with the HTML content of the entry.
    """
    entry = get_object_or_404(WikiEntry, id=entry_id)
    content = entry.content  # Valid HTML content
    return HttpResponse(content, content_type="text/html")
