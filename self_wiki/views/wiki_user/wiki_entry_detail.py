import html
from django.http import JsonResponse
from self_wiki.models import WikiEntry

def wiki_entry_detail(request, entry_id):
    """
    Returns the title and unescaped content of a wiki entry in JSON format by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        entry_id (int): ID of the wiki entry.

    Returns:
        JsonResponse: JSON with title and content, or 404 error if the entry does not exist.
    """
    try:
        entry = WikiEntry.objects.get(id=entry_id)
        data = {
            'title': entry.title,
            'content': html.unescape(entry.content),
        }
        return JsonResponse(data)
    except WikiEntry.DoesNotExist:
        return JsonResponse({'error': 'Entrada no encontrada'}, status=404)
