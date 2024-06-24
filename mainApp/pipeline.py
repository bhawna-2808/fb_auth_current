# # myapp/pipeline.py

# # from django.contrib.auth.models import User
# from .models import CustomUser
# from social_core.exceptions import AuthException

# def custom_create_user(strategy, details, user=None, *args, **kwargs):
#     """
#     Custom pipeline method to create a user if one does not exist.
#     """
#     if user:
#         return {'is_new': False}

#     fields = {
#         'username': details.get('username') or details.get('email').split('@')[0],
#         'email': details.get('email'),
#         'first_name': details.get('first_name'),
#         'last_name': details.get('last_name')
#     }

#     if not fields['email']:
#         raise AuthException(strategy.backend, 'Email is required to create a new user')

#     user = strategy.create_user(**fields)
#     return {
#         'is_new': True,
#         'user': user
#     }

# pipeline.py

from .models import CustomUser
from social_core.exceptions import AuthException

def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    Custom pipeline method to create a user if one does not exist.
    """
    if user:
        return {'is_new': False}

    fields = {
        'email': details.get('email'),
        'password': strategy.request_data().get('password'),
        'full_name': details.get('fullname'),
    }

    if not fields['email']:
        raise AuthException(strategy.backend, 'Email is required to create a new user')

    user = CustomUser.objects.create_user(email=fields['email'], password=fields['password'], full_name=fields['full_name'])
    return {
        'is_new': True,
        'user': user
    }
