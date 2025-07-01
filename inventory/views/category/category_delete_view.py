from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ...models import Category
from django.contrib import messages
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Categoria')
@login_required
def category_delete(request, pk):
    """
    Delete a category belonging to the logged-in user's company after confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the category to delete.

    Returns:
        HttpResponse: Redirects to category list after deletion or renders confirmation page.

    Raises:
        Http404: If the category does not exist or does not belong to the user's company.
    """
    # Get the category filtered by the user's company or return 404
    category = get_object_or_404(Category, pk=pk, company=request.user.userprofile.company)

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Categoría "{category_name}" eliminada exitosamente')
        return redirect('category-list')

    # Render confirmation page before deletion
    return render(request, 'category/category_confirm_delete.html', {'category': category})
