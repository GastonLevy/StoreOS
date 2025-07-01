from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...models import WikiCategory

@login_required
def delete_wiki_category(request, category_id):
    """
    Deletes a wiki category after confirmation.
    
    Accessible only to superusers.

    Args:
        request: HttpRequest object.
        category_id: ID of the category to delete.

    Returns:
        Redirects to the main page after deletion or shows the confirmation form.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    category = get_object_or_404(WikiCategory, id=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('wiki_home')

    return render(request, 'wiki_category/wiki_category_delete.html', {'category': category})
