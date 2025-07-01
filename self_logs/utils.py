from threading import local

"""
Utility to store and retrieve the current user in the context of the current thread.
"""

_user = local()

def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, 'value', None)
