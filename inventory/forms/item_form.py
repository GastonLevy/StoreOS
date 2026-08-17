from django import forms
from ..models import Item

MAX_PRICE = 99999999.99
MAX_QUANTITY = 99999999
MAX_COST = 99999999.99
MAX_PERCENTAGE = 999.99


class ItemForm(forms.ModelForm):
    """
    Form for creating and updating Item instances with validation.
    """

    class Meta:
        model = Item
        fields = [
            'name',
            'barcode',
            'quantity',
            'description',
            'price',
            'cost',
            'is_calculated',
            'percentage',
            'categories',
            'stockable',
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price > MAX_PRICE:
            raise forms.ValidationError(
                f'El precio no puede superar {MAX_PRICE}.'
            )

        return price

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')

        if cost is not None and cost > MAX_COST:
            raise forms.ValidationError(
                f'El costo no puede superar {MAX_COST}.'
            )

        return cost

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None and quantity > MAX_QUANTITY:
            raise forms.ValidationError(
                f'La cantidad no puede superar {MAX_QUANTITY}.'
            )

        return quantity

    def clean_percentage(self):
        percentage = self.cleaned_data.get('percentage')

        if percentage is not None and percentage > MAX_PERCENTAGE:
            raise forms.ValidationError(
                f'El porcentaje no puede superar {MAX_PERCENTAGE}%.'
            )

        return percentage

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')

        if not categories or categories.count() == 0:
            raise forms.ValidationError(
                'Debe seleccionar al menos una categoría.'
            )

        return categories

    def clean(self):
        cleaned_data = super().clean()

        is_calculated = cleaned_data.get('is_calculated')
        percentage = cleaned_data.get('percentage')

        if is_calculated and percentage is None:
            self.add_error(
                'percentage',
                'Debe ingresar un porcentaje si el precio se calcula automáticamente.'
            )

        return cleaned_data