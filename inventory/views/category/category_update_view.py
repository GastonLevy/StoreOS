from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...forms import CategoryForm
from ...models import Category
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Categoria')
def category_update(request, pk=None):
    """
    Create or update a Category.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): Primary key of the Category to update. If None, creates a new Category.

    Returns:
        HttpResponse: Redirects to category list on success or renders the form with errors.

    Raises:
        Http404: If pk is provided but no Category with that pk exists.
    """
    category = get_object_or_404(Category, pk=pk) if pk else None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría guardada correctamente.')
            return redirect('category-list')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category/category_form.html', {'form': form, 'category': category})
