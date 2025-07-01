from self_logs.utils import set_current_user
from django.http import HttpRequest, HttpResponse

class CurrentUserMiddleware:
    """
    Middleware to store the currently authenticated user in a thread-local variable.
    This allows access to the user from signals or other places where the request is not directly available.
    """

    def __init__(self, get_response: callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            set_current_user(request.user)
        else:
            set_current_user(None)

        return self.get_response(request)
