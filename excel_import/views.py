import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from users.models import Company
from inventory.models import Category, Item
from accounts.models import Person, Supplier, Debt
from checkout.models.cart_model import Cart

def process_category_sheet(data, company):
    """
    Process the 'Category' sheet data and update or create Category records.

    Args:
        data (pd.DataFrame): DataFrame containing category data.
        company (Company): Company instance to associate categories with.

    Raises:
        ValueError: If 'nombre' column is missing in the data.

    Returns:
        None
    """
    if 'nombre' not in data.columns:
        raise ValueError("El archivo debe contener una columna llamada 'nombre' en la pestaña 'Categoria'.")
    for _, row in data.iterrows():
        Category.objects.update_or_create(
            name=row['nombre'],
            company=company
        )


def process_item_sheet(data, company):
    """
    Process the 'Item' sheet data and update or create Item records.

    Args:
        data (pd.DataFrame): DataFrame containing item data.
        company (Company): Company instance to associate items with.

    Raises:
        ValueError: If any required column is missing in the data.

    Returns:
        None
    """
    required_columns = ['nombre', 'precio', 'cantidad', 'es_stockable', 'descripcion', 'categorias', 'costo']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"El archivo debe contener una columna llamada '{col}' en la pestaña 'Item'.")

    def clean_value(value):
        # Remove currency symbols and commas, convert to float, default 0.0
        if pd.notna(value):
            return float(str(value).replace('$', '').replace(',', '').strip())
        return 0.0

    def ensure_barcode(code):
        # Return zero-padded string of length 3, or None if not provided
        if pd.notna(code):
            code_str = str(code).strip()
            return code_str.zfill(3)
        return None

    unassigned_category, _ = Category.objects.get_or_create(name="Sin asignar", company=company)

    for _, row in data.iterrows():
        price = clean_value(row['precio'])
        cost = clean_value(row['costo'])
        quantity = row['cantidad'] if pd.notna(row['cantidad']) else 0

        # Normalize boolean values for stockable
        stockable_raw = row['es_stockable'] if pd.notna(row['es_stockable']) else False
        stockable = str(stockable_raw).lower() in ['true', '1', 't', 'y', 'yes']

        barcode = ensure_barcode(row['codigo_de_barras']) if 'codigo_de_barras' in data.columns else None

        item, created = Item.objects.update_or_create(
            name=row['nombre'],
            company=company,
            defaults={
                'barcode': barcode,
                'price': price,
                'quantity': quantity,
                'stockable': stockable,
                'description': row['descripcion'] if pd.notna(row['descripcion']) else '',
                'cost': cost
            }
        )

        # Process categories
        if pd.notna(row['categorias']):
            categories = [
                Category.objects.get_or_create(name=cat.strip(), company=company)[0]
                for cat in row['categorias'].split(',')
            ]
        else:
            categories = [unassigned_category]

        item.categories.set(categories)


def process_person_sheet(data, company):
    """
    Process the 'Cuenta Corriente' sheet data, updating Person and Debt records.

    Args:
        data (pd.DataFrame): DataFrame containing person and debt data.
        company (Company): Company instance to associate persons and debts with.

    Raises:
        ValueError: If any required column is missing in the data.

    Returns:
        None
    """
    required_columns = ['nombre', 'apellido', 'telefono', 'direccion', 'monto']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"El archivo debe contener una columna llamada '{col}' en la pestaña 'Cuenta Corriente'.")

    for _, row in data.iterrows():
        first_name = row['nombre'] if pd.notna(row['nombre']) and row['nombre'] != '' else '-'
        last_name = row['apellido'] if pd.notna(row['apellido']) and row['apellido'] != '' else '-'

        person, created = Person.objects.update_or_create(
            first_name=first_name,
            last_name=last_name,
            company=company,
            defaults={
                'phone': row['telefono'] if pd.notna(row['telefono']) else None,
                'address': row['direccion'] if pd.notna(row['direccion']) else ''
            }
        )
        if pd.notna(row['monto']):
            Debt.objects.create(
                person=person,
                amount=float(row['monto'])
            )


def process_supplier_sheet(data, company):
    """
    Process the 'Proveedor' sheet data and update or create Supplier records.

    Args:
        data (pd.DataFrame): DataFrame containing supplier data.
        company (Company): Company instance to associate suppliers with.

    Raises:
        ValueError: If any required column is missing in the data.

    Returns:
        None
    """
    required_columns = ['nombre_del_proveedor', 'contacto', 'correo_electronico', 'telefono', 'direccion']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"El archivo debe contener una columna llamada '{col}' en la pestaña 'Proveedor'.")

    for _, row in data.iterrows():
        Supplier.objects.update_or_create(
            name=row['nombre_del_proveedor'],
            company=company,
            defaults={
                'contact': row['contacto'] if pd.notna(row['contacto']) else None,
                'email': row['correo_electronico'] if pd.notna(row['correo_electronico']) else None,
                'phone': row['telefono'] if pd.notna(row['telefono']) else None,
                'address': row['direccion'] if pd.notna(row['direccion']) else ''
            }
        )


def cargar_excel_view(request):
    """
    View to handle Excel file upload and process its sheets.

    Handles POST requests with an Excel file and company ID.
    Reads sheets: 'Categoria', 'Item', 'Cuenta Corriente', and 'Proveedor'.
    Processes each sheet and returns JSON responses with success or error messages.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template for GET requests or JsonResponse for POST.
    """
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_excel')
        company_id = request.POST.get('company_id')

        if not archivo_excel or not company_id:
            return JsonResponse({'status': 'error', 'message': 'Faltan datos en el formulario.'})

        try:
            company = Company.objects.get(id=company_id)
            sheets = pd.read_excel(archivo_excel, sheet_name=None)

            if 'Categoria' in sheets:
                process_category_sheet(sheets['Categoria'], company)
            else:
                return JsonResponse({'status': 'error', 'message': "No se encontró la pestaña 'Categoria' en el archivo."})

            if 'Item' in sheets:
                process_item_sheet(sheets['Item'], company)
            else:
                return JsonResponse({'status': 'error', 'message': "No se encontró la pestaña 'Item' en el archivo."})

            if 'Cuenta Corriente' in sheets:
                process_person_sheet(sheets['Cuenta Corriente'], company)
            else:
                return JsonResponse({'status': 'error', 'message': "No se encontró la pestaña 'Cuenta Corriente' en el archivo."})

            if 'Proveedor' in sheets:
                process_supplier_sheet(sheets['Proveedor'], company)
            else:
                return JsonResponse({'status': 'error', 'message': "No se encontró la pestaña 'Proveedor' en el archivo."})

            return JsonResponse({'status': 'success', 'message': 'Datos cargados exitosamente.'})

        except Company.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f"Compañía con ID {company_id} no encontrada."})
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error procesando el archivo: {str(e)}"})

    return render(request, 'excel_check.html')
