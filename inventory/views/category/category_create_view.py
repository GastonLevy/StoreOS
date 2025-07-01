from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...forms import CategoryForm
from ...models import Category
from storeos.decorators import role_required

@role_required('Admin', 'Crear_Categoria')
def category_create(request):
    """
    Create a new category associated with the logged-in user's company.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to category list on success or renders form on failure.

    Raises:
        None explicitly, but form validation errors may occur.
    """
    # Get the user's profile
    user_profile = request.user.userprofile

    # Check if the user has a company associated
    if not user_profile.company:
        messages.error(request, 'Debes asociar una compañía a tu perfil antes de crear una categoría.')
        return redirect('profile')  # Redirect to profile to associate a company

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        form.user_profile = user_profile  # Pass user profile to form (if used in form logic)

        if form.is_valid():
            category = form.save(commit=False)
            category.company = user_profile.company  # Assign company from user profile
            category.save()

            messages.success(request, 'Categoría creada exitosamente')
            return redirect('category-list')  # Redirect to category list
        else:
            messages.error(request, 'Hubo un error al crear la categoría. Verifica los datos.')
    else:
        form = CategoryForm()

    # Render category creation form
    return render(request, 'category/category_form.html', {'form': form})
