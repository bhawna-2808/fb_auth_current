# myapp/pipeline.py

from .models import CustomUser  # Import your CustomUser model
from social_core.exceptions import AuthException

def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    Custom pipeline method to create a user if one does not exist.
    """
    if user:
        return {'is_new': False}

    fields = {
        'username': details.get('username') or details.get('email').split('@')[0],
        'email': details.get('email'),
        'first_name': details.get('first_name'),
        'last_name': details.get('last_name')
    }

    if not fields['email']:
        raise AuthException(strategy.backend, 'Email is required to create a new user')

    # Create CustomUser instead of User
    user = CustomUser.objects.create_user(**fields)

    return {
        'is_new': True,
        'user': user
    }
