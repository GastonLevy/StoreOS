from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...forms import WikiCategoryForm

@login_required
def add_wiki_category(request):
    """
    Adds a new wiki category.

    Accessible only to superusers.

    Args:
        request: HttpRequest object.

    Returns:
        Redirects to the category list if the form is valid,
        or displays the form to add a category.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    if request.method == 'POST':
        form = WikiCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_wiki_category')
    else:
        form = WikiCategoryForm()

    return render(request, 'wiki_category/wiki_category_form.html', {'form': form})
