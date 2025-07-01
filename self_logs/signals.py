from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from self_logs.models import ActionLog
from self_logs.utils import get_current_user

# Models to watch for logging
WATCHED_MODELS = [
    'Debt', 'Person', 'SupplierEntry', 'Supplier', 'EntryPack',
    'CashRegister', 'CashMovement', 'Cart', 'CartLine', 'PaymentMethod',
    'Category', 'Item', 'ReceptionLog', 'Reception', 'WikiCategory',
    'WikiEntry',
]

def format_instance_data(instance):
    """
    Formats model instance fields into a readable string,
    excluding internal fields like _state.
    """
    if not instance:
        return ''
    formatted_data = []
    for field, value in instance.__dict__.items():
        if field != '_state':
            formatted_data.append(f"{field.capitalize()}: {value}")
    return "\n".join(formatted_data)

@receiver(pre_save)
def log_edit(sender, instance, **kwargs):
    """
    Logs an entry when a watched model instance is edited.
    Compares the previous state with the new one.
    """
    if sender.__name__ not in WATCHED_MODELS or not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    ActionLog.objects.create(
        company=getattr(instance, 'company', None),
        user=get_current_user(),
        action='Editado',
        model_name=sender.__name__,
        object_id=instance.pk,
        details=f"Antes:\n{format_instance_data(old_instance)}\n\nAhora:\n{format_instance_data(instance)}",
    )

@receiver(post_save)
def log_create(sender, instance, created, **kwargs):
    """
    Logs an entry when a new watched model instance is created.
    """
    if sender.__name__ not in WATCHED_MODELS:
        return

    if created:
        ActionLog.objects.create(
            company=getattr(instance, 'company', None),
            user=get_current_user(),
            action='Creado',
            model_name=sender.__name__,
            object_id=instance.pk,
            details=f"Datos:\n{format_instance_data(instance)}",
        )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    """
    Logs an entry when a watched model instance is deleted.
    """
    if sender.__name__ not in WATCHED_MODELS:
        return

    ActionLog.objects.create(
        company=getattr(instance, 'company', None),
        user=get_current_user(),
        action='Eliminado',
        model_name=sender.__name__,
        object_id=instance.pk,
        details=f"Datos:\n{format_instance_data(instance)}",
    )
