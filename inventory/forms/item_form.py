from django import forms
from ..models import Item

MAX_PRICE = 99999999.99  # Maximum limit for price
MAX_QUANTITY = 99999999  # Maximum limit for quantity
MAX_COST = 99999999.99  # Maximum limit for cost

class ItemForm(forms.ModelForm):
    """
    Form for creating and updating Item instances with validation.

    Methods:
        clean_price() -> Decimal:
            Validates that the price does not exceed MAX_PRICE.
            Raises:
                ValidationError: If price is greater than MAX_PRICE.
            Returns:
                Decimal: The validated price value.

        clean_cost() -> Decimal:
            Validates that the cost does not exceed MAX_COST.
            Raises:
                ValidationError: If cost is greater than MAX_COST.
            Returns:
                Decimal: The validated cost value.

        clean_quantity() -> int:
            Validates that the quantity does not exceed MAX_QUANTITY.
            Raises:
                ValidationError: If quantity is greater than MAX_QUANTITY.
            Returns:
                int: The validated quantity value.

        clean_categories() -> QuerySet:
            Validates that at least one category is selected.
            Raises:
                ValidationError: If no categories are selected.
            Returns:
                QuerySet: The validated categories queryset.
    """
    class Meta:
        model = Item
        fields = ['name', 'barcode', 'quantity', 'description', 'price', 'cost', 'categories', 'stockable']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price > MAX_PRICE:
            raise forms.ValidationError(f'El precio no puede superar {MAX_PRICE}.')
        return price

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost > MAX_COST:
            raise forms.ValidationError(f'El costo no puede superar {MAX_COST}.')
        return cost

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity > MAX_QUANTITY:
            raise forms.ValidationError(f'La cantidad no puede superar {MAX_QUANTITY}.')
        return quantity

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories or categories.count() == 0:
            raise forms.ValidationError('Debe seleccionar al menos una categoría.')
        return categories
