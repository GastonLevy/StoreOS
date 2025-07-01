from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...forms import WikiCategoryForm
from ...models import WikiCategory

@login_required
def edit_wiki_category(request, pk):
    """
    Edits an existing wiki category.
    Accessible only to superusers.

    Args:
        request (HttpRequest): HTTP request object.
        pk (int): ID of the category to edit.

    Returns:
        HttpResponse: Renders form or redirects to category list.
        HttpResponseForbidden: If the user is not a superuser.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    category = get_object_or_404(WikiCategory, pk=pk)
    
    if request.method == 'POST':
        form = WikiCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_wiki_category')
    else:
        form = WikiCategoryForm(instance=category)

    return render(request, 'wiki_category/wiki_category_form.html', {
        'form': form,
        'category': category,
    })
