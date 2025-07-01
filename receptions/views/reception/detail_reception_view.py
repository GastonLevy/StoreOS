from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse
from xhtml2pdf import pisa
from ...models import Reception
from storeos.decorators import role_required

class ReceptionStatusForm(ModelForm):
    """
    Form for editing the status of a Reception.

    Fields:
        status (str): The status of the reception.
    """
    class Meta:
        model = Reception
        fields = ['status']

def render_to_pdf(template_src, context_dict):
    """
    Render a template to PDF using xhtml2pdf.

    Args:
        template_src (str): Path to the template to render.
        context_dict (dict): Context data for the template.

    Returns:
        BytesIO or None: PDF file in memory if successful, None otherwise.
    """
    from django.template.loader import render_to_string
    from io import BytesIO

    # Render the HTML content from the template and context
    html = render_to_string(template_src, context_dict)
    
    # Create a memory buffer for the PDF output
    buffer = BytesIO()

    # Generate the PDF from the HTML content
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), buffer)
    if not pdf.err:
        buffer.seek(0)
        return buffer
    return None

@role_required('Admin', 'Cajero', 'Detalle_Recepcion')
def reception_detail(request, pk):
    """
    View to display and update details of a Reception, including status change and PDF download.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Reception to display.

    Returns:
        HttpResponse: Rendered page or PDF file response.

    Raises:
        Http404: If the Reception does not exist for the user's company.
    """
    company = request.user.userprofile.company
    reception = get_object_or_404(Reception, pk=pk, company=company)

    is_completed = reception.status == 'completed'

    if request.method == "POST" and not is_completed:
        form = ReceptionStatusForm(request.POST, instance=reception)
        if form.is_valid():
            form.save()
            messages.success(request, "El estado de la recepción se ha actualizado correctamente.")
            return redirect('reception-detail', pk=reception.pk)
        else:
            messages.error(request, "Hubo un error al actualizar el estado.")
    else:
        form = ReceptionStatusForm(instance=reception)
        if is_completed:
            # Disable the status field if reception is completed
            form.fields['status'].widget.attrs['disabled'] = True

    if request.GET.get('download_pdf'):
        context = {
            'reception': reception,
            'is_completed': is_completed,
            'form': form,
        }
        pdf = render_to_pdf('reception/reception_pdf_template.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename={}_{}_{}.pdf'.format(
                reception.person,  # Cliente
                reception.received_by.get_full_name(),  # Persona que recibió
                reception.reception_date.strftime('%d_%m_%Y')  # Fecha
            )
            return response

    return render(
        request,
        'reception/reception_detail.html',
        {
            'reception': reception,
            'form': form,
            'is_completed': is_completed,
        }
    )
