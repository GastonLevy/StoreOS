from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe

from self_wiki.forms import WikiEntryForm
from self_wiki.models import WikiEntry, WikiCategory

@login_required
def edit_wiki_entry(request, category_id, entry_id):
    """
    Allows editing a wiki entry within a specific category.
    Accessible only to superusers.

    Args:
        request (HttpRequest): HTTP request object.
        category_id (int): ID of the associated category.
        entry_id (int): ID of the wiki entry to edit.

    Returns:
        HttpResponse: Renders the edit form or redirects after saving.
        HttpResponseForbidden: If the user is not a superuser.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    category = get_object_or_404(WikiCategory, id=category_id)
    entry = get_object_or_404(WikiEntry, id=entry_id)

    if request.method == 'POST':
        form = WikiEntryForm(request.POST, instance=entry)
        if form.is_valid():
            wiki_entry = form.save(commit=False)
            wiki_entry.category = category
            wiki_entry.content = mark_safe(wiki_entry.content)  # Mark content safe to allow HTML
            wiki_entry.save()
            return redirect('wiki_category-detail', pk=category.id)
    else:
        form = WikiEntryForm(instance=entry)

    return render(request, 'wiki_entry/wiki_entry_form.html', {
        'form': form,
        'category': category,
        'entry': entry
    })
