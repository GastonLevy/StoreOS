from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from ...models import Person
from ...forms import PersonForm
from storeos.decorators import role_required


@role_required('Admin', 'Modificar_Cuenta')
def account_update(request, pk):
    """
    Update a Person's account if the person belongs to the user's company.
    """
    person = get_object_or_404(Person, pk=pk)

    if person.company != request.user.userprofile.company:
        raise Http404("No tienes permiso para editar esta persona.")

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('account-list')
    else:
        form = PersonForm(instance=person)

    return render(request, 'accounts/account_form.html', {
        'form': form,
        'person': person
    })