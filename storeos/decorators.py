from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    """
    Decorator to restrict access to views based on user roles.

    Allows access only if the user is authenticated and is a superuser
    or belongs to any of the specified groups.

    Args:
        *roles (str): Names of allowed groups.

    Returns:
        The protected view function.

    Raises:
        PermissionDenied if the user lacks permission.
    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Allow superuser without further checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = request.user.groups.values_list('name', flat=True)
            # Check if user belongs to any allowed role
            if not any(role in user_groups for role in roles):
                raise PermissionDenied("You do not have permission to access this view.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
