def user_roles(request):
    """
    Añade los roles del usuario al contexto de las plantillas.
    """
    if request.user.is_authenticated:
        return {"user_groups": request.user.groups.values_list('name', flat=True)}
    return {"user_groups": []}
