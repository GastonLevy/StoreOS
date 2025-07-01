from django.contrib import admin
from .models import Debt, Person, SupplierEntry, EntryPack, Supplier

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    """
    Admin configuration for Debt model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields to enable search.
        list_filter (tuple): Fields to enable filtering.
        ordering (tuple): Default ordering of the list view.
        readonly_fields (tuple): Fields set as read-only in admin form.
    """
    list_display = ('person', 'amount', 'due_date', 'status', 'cart')  # Show relevant fields
    search_fields = ('person__first_name', 'person__last_name', 'cart__id')  # Search by person's name or cart ID
    list_filter = ('status', 'person', 'cart')  # Filter by status, person, and cart
    ordering = ('-due_date',)  # Order by due_date descending
    readonly_fields = ('status',)  # Read-only field for debt status


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin configuration for Person model.

    Attributes:
        list_display (tuple): Fields to display.
        search_fields (tuple): Fields for search.
        list_filter (tuple): Fields for filtering.
        ordering (tuple): Default ordering.
        readonly_fields (tuple): Read-only fields.
    """
    list_display = ('first_name', 'last_name', 'phone', 'address', 'company')
    search_fields = ('first_name', 'last_name', 'company__name')
    list_filter = ('company',)
    ordering = ('last_name',)
    readonly_fields = ('total_debt',)

    def total_debt(self, obj):
        """
        Returns the total debt for the person.

        Args:
            obj (Person): Person instance.

        Returns:
            Decimal: Total debt amount.
        """
        return obj.total_debt()
    total_debt.short_description = 'Deuda Total'


@admin.register(SupplierEntry)
class SupplierEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for SupplierEntry model.
    """
    list_display = ('supplier', 'item_name', 'item_code', 'quantity', 'date', 'company')
    search_fields = ('supplier__name', 'item_name', 'item_code')
    list_filter = ('supplier', 'company')
    ordering = ('-date',)


@admin.register(EntryPack)
class EntryPackAdmin(admin.ModelAdmin):
    """
    Admin configuration for EntryPack model.
    """
    list_display = ('supplier', 'description', 'created_at', 'company')
    search_fields = ('supplier__name', 'description')
    list_filter = ('supplier', 'company')
    ordering = ('-created_at',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for Supplier model.
    """
    list_display = ('name', 'contact', 'email', 'phone', 'company')
    search_fields = ('name', 'contact', 'company__name')
    list_filter = ('company',)
    ordering = ('name',)

    def get_receipt(self, obj):
        """
        Provides a clickable link to the supplier's receipt if available.

        Args:
            obj (Supplier): Supplier instance.

        Returns:
            str: HTML anchor tag with link or string if no receipt.

        Raises:
            None explicitly.
        """
        if obj.receipt:
            return f'<a href="{obj.receipt.url}" target="_blank">Ver remito</a>'
        return "Sin remito"
    get_receipt.allow_tags = True
    get_receipt.short_description = "Remito"

    list_display += ('get_receipt',)
