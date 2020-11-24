from django.contrib.auth import backends
from .models import User

class AuthCustom(backends.ModelBackend):
    def authenticate(self,request, username=None, password=None):
        """
        Description: Производит аутентификацию, при успехе возвращает пользователя, иначе None.
        Args: request - запрос пользователя, username - email пользователя, password - пароль пользователя.
        """
        login_valid = bool(User.objects.get(Email=username).Email==username)
        pwd_valid = bool(User.objects.get(Email=username).Password==password)
        if login_valid and pwd_valid:
            user=User.objects.get(Email=username)
            return user
        return None

    def get_user(self,id):
        """
        Description: Получает пользователя из базы данных по id.
        Args: id - id пользователя.
        """
        return User.objects.get(id=id)