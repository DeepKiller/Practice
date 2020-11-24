from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpRequest
from django.contrib.auth.password_validation import validate_password,ValidationError
from django.contrib.auth import authenticate,login
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login
from .models import User
from re import match
import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

@require_http_methods(['POST'])
def Registration(request):
    """
    Description: Проверяет корректность полученных в запросе данных(email,пароль), при корректности регистрирует нового пользователя.
    Args: request - запрос от клиента с методом POST содержащий в себе Email и Password.
    """
    try:
        Email = request.POST.get('Email')
        Password = password=request.POST.get('Password')
    except:
        return HttpRequest('Bad request',status=400)
    ValidPass,Error=CheckPassword(Password)
    if ValidPass:
        if  CheckMail(Email):
            user = User.objects.create_user(Email,Password)
            return HttpResponse("Registred",status=201)
        else:
            return HttpResponse("Wrong email")
    else:
        return HttpResponse("Wrong password: " + Error.messages[0])

def CheckMail(email):
    """
    Description: Проверяет строку на соответствие шаблону, и наличие в базе данных.
    Args: email - строка для проверки.
    """
    if match(r"\w+@\w+.\w+",email):
        DBEmail = User.objects.filter(Email=email)
        if not DBEmail:
            return True
    return False

def CheckPassword(password):
    """
    Description: Проверка строки стандартным обработчиком валидации паролей.
    Args: password - строка для проверки.
    """
    try:
        validate_password(password)
        return (True,None)
    except ValidationError as error:
        return (False,error)

@require_http_methods(['POST'])
def Login(request):
    """
    Description: Производит аутентификацию пользователя с помощью полученных в запросе данных(email,пароль), после аутентификации регистрирует новую сессию пользователя.
    Args: request - запрос от клиента с методом POST содержащий в себе Email и Password.
    """
    try:
        user = authenticate(username=request.POST.get('Email'),password=request.POST.get('Password'))
    except:
        return HttpResponse('Bad request', status=400)
    if not user==None:
        user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
        login(request,user)
        return HttpResponse("Login")
    else:
        return HttpResponse("Login failed", status=401)

@require_http_methods(['DELETE'])    
def DeleteUser(request):
    """
    Description: Удаляет пользователя с помощью полученных в запросе данных.
    Args: request - запрос от клиента с методом DELETE содержащий в себе Email.
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            data = json.loads(request.read().decode("UTF-8").replace('\'','\"'))
            User.objects.get(Email=data['Email']).delete()
            return HttpResponse("Deleted")
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['GET'])
def ViewUsers(request):
    """
    Description: Отображает список пользователей на указанной странице.
    Args: request - запрос от клиента с методом GET содержащий в себе page (номер необходимой страницы).
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            users = User.objects.all().order_by('id')
            paginator = Paginator(users,15)
            try:
                page = paginator.page(request.GET.get('page'))
            except PageNotAnInteger:
                return HttpResponse("Page not an integer",status=400)
            except EmptyPage:
                return HttpResponse("Empty page",status=400)
            return HttpResponse(page.object_list)
        else: 
            return HttpResponse("No permision",status=403)
    else:
        return HttpResponse("Not logged in",status=401)