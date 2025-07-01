from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe
from ...forms import WikiEntryForm
from ...models import WikiCategory

@login_required
def create_wiki_entry(request, category_id):
    """
    Creates a new wiki entry within a specific category.
    Accessible only to superusers.

    Args:
        request (HttpRequest): HTTP request object.
        category_id (int): ID of the category where the entry will be created.

    Returns:
        HttpResponse: Renders the form or redirects to category detail after creation.
        HttpResponseForbidden: If the user is not a superuser.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    category = get_object_or_404(WikiCategory, id=category_id)

    if request.method == 'POST':
        form = WikiEntryForm(request.POST)
        if form.is_valid():
            wiki_entry = form.save(commit=False)
            wiki_entry.category = category
            wiki_entry.content = mark_safe(wiki_entry.content)  # Mark content as safe HTML
            wiki_entry.save()
            return redirect('wiki_category-detail', pk=category.id)
    else:
        form = WikiEntryForm()

    return render(request, 'wiki_entry/wiki_entry_form.html', {
        'form': form,
        'category': category
    })
