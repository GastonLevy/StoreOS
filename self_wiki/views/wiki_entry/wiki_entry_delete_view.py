from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...models import WikiEntry, WikiCategory

@login_required
def delete_wiki_entry(request, category_id, entry_id):
    """
    Allows deleting a wiki entry within a specific category.
    Accessible only to superusers.

    Args:
        request (HttpRequest): HTTP request object.
        category_id (int): ID of the associated category.
        entry_id (int): ID of the wiki entry to delete.

    Returns:
        HttpResponse: Renders deletion confirmation or redirects after deletion.
        HttpResponseForbidden: If the user is not a superuser.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    category = get_object_or_404(WikiCategory, id=category_id)
    wiki_entry = get_object_or_404(WikiEntry, id=entry_id)

    if request.method == 'POST':
        wiki_entry.delete()
        return redirect('wiki_category-detail', pk=category.id)  # Redirect to category detail after deletion

    return render(request, 'wiki_entry/wiki_entry_confirm_delete.html', {
        'wiki_entry': wiki_entry,
        'category': category
    })
