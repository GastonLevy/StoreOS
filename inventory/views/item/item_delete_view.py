from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ...models import Item
from django.contrib import messages
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Producto')
def item_delete(request, pk):
    """
    Handle deletion of an item ensuring it belongs to the logged-in user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Item to delete.

    Returns:
        HttpResponse: Redirects to the item list on successful deletion or after POST,
                        or renders a confirmation page on GET.

    Raises:
        Http404: If the item does not exist or does not belong to the user's company.
        Exception: Propagates exceptions during deletion to show error message.
    """
    # Get the user's profile
    user_profile = request.user.userprofile

    # Get the item ensuring it belongs to the user's company
    item = get_object_or_404(Item, pk=pk, company=user_profile.company)

    if request.method == 'POST':
        try:
            item_name = item.name
            item.delete()
            messages.success(request, f'Ítem "{item_name}" eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Hubo un problema al eliminar el ítem: {str(e)}')
        return redirect('item-list')

    # Render confirmation page for deletion
    return render(request, 'item/item_confirm_delete.html', {'item': item})
