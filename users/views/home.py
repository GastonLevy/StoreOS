from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Main system view. Requires user to be logged in.
@login_required
def home_view(request):
    """
    Main system view. Requires the user to be logged in.
    """
    return render(request, 'home.html')
