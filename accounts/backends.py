from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to allow users to log in using their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # We treat the 'username' parameter as the email address
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If not found by email, try falling back to standard username
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        return None
