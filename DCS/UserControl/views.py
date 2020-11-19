from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpRequest
from django.contrib.auth.password_validation import validate_password,ValidationError
from .models import User
from django.utils import timezone

@require_http_methods(['POST'])
def Registration(request):
    Params = request.body.decode('UTF-8')
    Email = Params.split('&')[0].split('=')[-1]
    Password = Params.split('&')[-1].split('=')[-1]
    if CheckPassword(Password):
        if  CheckMail(Email):
            user = User()
            user.Email = Email
            user.Password = Password
            timezone.activate("Europe/Moscow")
            user.DateCreated,user.DateUpdated = timezone.now(),timezone.now()
            user.save()
            return HttpResponse("Registred")
            

def CheckMail(email):
    return True


def CheckPassword(password):
    try:
        validate_password(password)
        return True
    except ValidationError as error:
        return False