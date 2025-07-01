from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import logging

logger = logging.getLogger(__name__)

def error_view(request, exception=None):
    """
    Generic view to handle HTTP errors. Returns a template with the corresponding status code.
    """
    if isinstance(exception, Http404):
        code = 404
    elif isinstance(exception, PermissionDenied):
        code = 403
    elif isinstance(exception, SuspiciousOperation):
        code = 400
    elif isinstance(exception, Exception):
        code = 500
        logger.error("Unexpected error", exc_info=exception)
    else:
        code = 404

    # Renders the error template with the appropriate status code
    return render(request, 'error.html', {'code': code}, status=code)
