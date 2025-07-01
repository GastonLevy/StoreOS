from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from ...models import Debt, Person
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Crear_Deuda')
def create_debt(request):
    """
    Create a debt record associated with a person belonging to the user's company.

    Args:
        request (HttpRequest): The HTTP request object with POST data containing:
            - person (str): ID of the Person to whom the debt belongs.
            - amount (str): Amount of the debt.
            - due_date (str or None): Optional due date for the debt.
            - action (str): 'debitar' for debit (negative amount), 'acreditar' for credit (positive amount).

    Returns:
        HttpResponseRedirect: Redirects to the person's account detail page on success or on invalid data.
        HttpResponseForbidden: If the person belongs to a different company.

    Raises:
        None explicitly, but will redirect on missing or invalid data.
    """
    user_company = request.user.userprofile.company

    # Get the person by ID and check company association
    person_id = request.POST.get('person')
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return redirect('account-list')  # Redirect if person doesn't exist

    if person.company != user_company:
        return HttpResponseForbidden("No puedes crear deudas para personas de otra compañía.")

    # Process form only on POST method
    if request.method == 'POST':
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date') or None  # Set None if no due date provided
        action = request.POST.get('action')

        if not amount:
            return redirect('account-detail', pk=person.id)  # Redirect if amount missing

        amount = float(amount)
        if action == 'debitar':
            amount = -abs(amount)  # Ensure amount is negative
        elif action == 'acreditar':
            amount = abs(amount)   # Ensure amount is positive

        # Create the debt entry
        Debt.objects.create(
            person=person,
            amount=amount,
            due_date=due_date,
            status='pendiente',
            company=user_company
        )

        # Redirect to person's account detail
        return redirect('account-detail', pk=person.id)

    # Redirect to person's account detail if not POST
    return redirect('account-detail', pk=person.id)
