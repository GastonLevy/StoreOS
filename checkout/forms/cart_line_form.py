from django import forms
from ..models import CartLine
from inventory.models import Item

class CartLineForm(forms.Form):
    """
    Form to add or update a CartLine.

    Fields:
        item_id (int): ID of the item to add. Hidden input.
        quantity (float): Quantity of the item; must be > 0.

    Methods:
        clean_quantity():
            Validates that quantity is greater than zero.

        clean_item_id():
            Validates that the provided item_id corresponds to an existing Item.

    Raises:
        ValidationError: If quantity <= 0 or item_id does not exist.
    """

    item_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)  # Field for the item ID
    quantity = forms.FloatField(
        required=True,
        min_value=0.0001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0.0001',
            'step': '0.0001'
        })
    )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor que cero.')
        return quantity

    def clean_item_id(self):
        item_id = self.cleaned_data.get('item_id')
        try:
            Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise forms.ValidationError('El producto seleccionado no es válido.')
        return item_id


class TemporaryProductForm(forms.Form):
    """
    Form for adding a temporary product (not in inventory).

    Fields:
        temp_name (str): Name of the temporary product.
        temp_price (float): Price of the temporary product; must be > 0.
        temp_quantity (float): Quantity of the temporary product; must be > 0.

    Raises:
        ValidationError: If any of the numeric fields are <= 0.
    """

    temp_name = forms.CharField(required=True, max_length=255)
    temp_price = forms.FloatField(required=True, min_value=0.0001)
    temp_quantity = forms.FloatField(required=True, min_value=0.0001)
