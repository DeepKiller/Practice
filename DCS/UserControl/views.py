from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpRequest
from django.contrib.auth.password_validation import validate_password,ValidationError
from django.contrib.auth import login,authenticate
from .models import User
from django.utils import timezone
from re import match

@require_http_methods(['POST'])
def Registration(request):
    Email = request.body.decode().split("&")[0].split('=')[1]
    Password = request.body.decode().split("&")[1].split('=')[1]
    if (CheckPassword(Password)[0]):
        if  CheckMail(Email):
            user = User()
            user.Email = Email
            user.Password = Password
            timezone.activate("Europe/Moscow")
            user.DateCreated,user.DateUpdated = timezone.now(),timezone.now()
            user.save()
            return HttpResponse("Registred",status=201)
        else:
            return HttpResponse("Wrong email")
    else:
        return HttpResponse("Wrong password: " + CheckPassword(Password)[1].messages[0])

def CheckMail(email):
    if match(r"\w+@\w+.\w+",email):
        DBEmail = User.objects.filter(Email=email)
        if not DBEmail:
            return True
    return False

def CheckPassword(password):
    try:
        validate_password(password)
        return True
    except ValidationError as error:
        return (False,error)

def Login(request):
    user = authenticate(username=request.body.decode().split("&")[0].split('=')[1],password=request.body.decode().split("&")[1].split('=')[1])
    if not user==None:
        login(request,user)
        return HttpResponse("Login")
    else:
        return HttpResponse("Login failed")