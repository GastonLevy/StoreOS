from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Crea roles y asigna permisos'

    def handle(self, *args, **kwargs):
        # Crear los grupos
        groups = [
            'Admin',
            'Cajero',
            'Cerrar_Caja',
            'Crear_Movimiento_Caja',
            'Detalle_Caja',
            'Listar_Caja',
            'Crear_Carro',
            'Eliminar_Carro',
            'Detalle_Carro',
            'Vaciar_Carro',
            'Finalizar_Carro',
            'Listar_Carro',
            'Eliminar_Linea_Carro',
            'Crear_Producto',
            'Eliminar_Producto',
            'Detalle_Producto',
            'Listar_Producto',
            'Buscar_Producto',
            'Modificar_Producto',
            'Crear_Categoria',
            'Eliminar_Categoria',
            'Detalle_Categoria',
            'Listar_Categoria',
            'Modificar_Categoria',
            'Crear_Cuenta',
            'Eliminar_Cuenta',
            'Detalle_Cuenta',
            'Listar_Cuenta',
            'Crear_Deuda',
            'Eliminar_Deuda',
            'Modificar_Deuda',
            'Crear_Proveedor',
            'Eliminar_Proveedor',
            'Detalle_Proveedor',
            'Listar_Proveedor',
            'Modificar_Proveedor',
            'Crear_Entrada_Proveedor',
            'Eliminar_Entrada_Proveedor',
            'Crear_Entrada_Grupo_Proveedor',
            'Eliminar_Entrada_Grupo_Proveedor',
            'Detalle_Entrada_Grupo_Proveedor',
            'Modificar_Entrada_Grupo_Proveedor',
            'Crear_Recepcion',
            'Detalle_Recepcion',
            'Listar_Recepcion',
            'Cyber',
            'Cyber_Admin',
            'Cyber_Crear_Editar_Dispositivo',
        ]

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(f'Grupo "{group_name}" creado: {created}')

        # Asignar permisos a los grupos
        # O puedes especificar permisos según el modelo
        permissions = Permission.objects.all()
        for group in groups:
            group_obj = Group.objects.get(name=group)
            # Asigna permisos a cada grupo (esto se hace según las necesidades)
            # Este ejemplo asigna todos los permisos a cada grupo
            for perm in permissions:
                group_obj.permissions.add(perm)
            self.stdout.write(f'Permisos asignados al grupo "{group}"')
