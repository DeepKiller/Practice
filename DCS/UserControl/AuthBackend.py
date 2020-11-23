from django.contrib.auth import backends
from .models import User

class AuthCustom(backends.ModelBackend):
    def authenticate(self,request, username=None, password=None):
        login_valid = bool(User.objects.get(Email=username).Email==username)
        pwd_valid = bool(User.objects.get(Email=username).Password==password)
        if login_valid and pwd_valid:
            user=User.objects.get(Email=username)
            return user
        return None

    def get_user(self,id):
        return User.objects.get(id=id)