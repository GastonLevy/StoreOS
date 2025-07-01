from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from ...models import Debt
from ...forms import DebtUpdateForm
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Deuda')
def debt_update(request, pk):
    """
    Update a Debt instance associated with a Person in the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Debt to update.

    Returns:
        HttpResponse: Redirects to the associated person's account detail on successful update,
                      or renders the debt update form if GET or form invalid.

    Raises:
        Http404: If the debt is not associated with the user's company.
    """
    debt = get_object_or_404(Debt, pk=pk)

    # Check if the debt belongs to the same company as the logged-in user
    if debt.person.company != request.user.userprofile.company:
        raise Http404("No tienes permiso para editar esta deuda.")

    if request.method == 'POST':
        # Process the form with POST data
        form = DebtUpdateForm(request.POST, instance=debt)
        if form.is_valid():
            # Save the updated amount explicitly (optional, form.save() alone would suffice)
            amount = form.cleaned_data['amount']
            form.instance.amount = amount
            form.save()

            # Redirect to the associated person's account detail
            return redirect('account-detail', pk=debt.person.id)
        else:
            # Debug: print form errors if validation fails
            print(form.errors)
    else:
        # Initialize form with the existing debt data for GET requests
        form = DebtUpdateForm(instance=debt)

    # Pass form, debt, and associated person to template context
    return render(request, 'accounts/account_debt_update.html', {'form': form, 'debt': debt, 'person': debt.person})
