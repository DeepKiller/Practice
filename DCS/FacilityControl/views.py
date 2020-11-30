from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse,JsonResponse
from string import ascii_letters,digits
from django.utils import timezone
from random import choices
import json

from .models import Facility
from UserControl.models import User
# Create your views here.
@require_http_methods(['POST'])
def Create(request):
    """
    Description: Метод создания новой установки из полученных данных.
    Args: request - запрос пользователя с методом POST, содержащий в себе: 
    Name - название, 
    Description - описание, 
    SerialNumber - серийный номер, 
    FirmwareVersion - версия прошивки.
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            data = json.loads(request.body)
            AllDigits = ascii_letters+digits
            UIN ='zCO2-'+''.join(choices(AllDigits, k=12))
            timezone.activate("Europe/Moscow")
            now = timezone.now()
            try:
                facility = Facility(
                    UIN=UIN,Name=data['Name'],
                    Description=data['Description'],
                    SerialNumber=data['SerialNumber'],
                    FirmwareVersion=data['FirmwareVersion'],
                    FirmwareLastUpdateDate=now,
                    DateCreated=now,
                    DateUpdated=now
                    ).save()
                return HttpResponse("Created",status=201)
            except:
                return HttpResponse("Bad request",status=400)
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['DELETE'])
def Delete(request):
    """
    Description: Удаляет установку с помощью полученных в запросе данных.
    Args: request - запрос от клиента с методом DELETE содержащий в себе id установки для удаления.
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            try:
                Facility.objects.get(id=json.loads(request.body)['id']).delete()
                return HttpResponse("Deleted")
            except:
                return HttpResponse("Object not found",status=404)
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['PUT'])
def Change(request):
    """
    Description: Метод изменения установки
    Args: request - запрос от клиента с методом PUT содержащий id установки для изменения и поля для изменения.
    """
    timezone.activate("Europe/Moscow")
    now = timezone.now()
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            fields = json.loads(request.body)['fields']
            id = json.loads(request.body)['id']
            facility = Facility.objects.get(id=id)
            notapplied = ''
            for field,value in fields.items():
                if hasattr(facility,field):
                    if field!='User':
                        setattr(facility,field,value)
                    else:
                        try:
                            setattr(facility,field,User.objects.get(Email=value))
                        except User.DoesNotExist:
                            setattr(facility,field,None)
                            setattr(facility,'InUse',False)
                else:
                    notapplied+=field+' '
            if "FirmwareVersion" in fields:
                setattr(facility,"FirmwareLastUpdateDate",now)
            setattr(facility,'DateUpdated',now)
            facility.save()
            if notapplied == '':
                return HttpResponse('Changed')
            else:
                return HttpResponse('Changed, but not applied: '+notapplied)
        else:
            fields = json.loads(request.body)
            facility = Facility.objects.get(User=request.user)
            atrribs = ('id','Name','Description','DeviceMode','NetworkMode','LastCO2Value','NightModeEnabled','NightModeAuto','NightModeFrom','NightModeTo')
            for field,value in fields.items():
                if hasattr(facility,field) and field in atrribs:
                    setattr(facility,field,value)
            setattr(facility,'DateUpdated',now)
            facility.save()
            return HttpResponse('Changed')
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['GET'])
def View(request):
    """
    Description: Отображает список установок на указанной странице. Для администратора для запрошенной установки, для пользователя для привязанной.
    Args: request - запрос от клиента с методом GET содержащий в себе page (номер необходимой страницы).
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            facs = Facility.objects.all().order_by('id')
            paginator = Paginator(facs,15)
            try:
                data = json.loads(request.body)
                page = paginator.page(data['page'])
            except PageNotAnInteger:
                return HttpResponse("Page not an integer",status=400)
            except EmptyPage:
                return HttpResponse("Empty page",status=400)
            resp={}
            for fac in page.object_list:
                resp['Facility_'+str(fac.id)]={
                    'UIN':fac.UIN,
                    'Name': fac.Name,
                    'Description':fac.Description,
                    'SerialNumber':fac.SerialNumber,
                    'FirmwareVersion':fac.FirmwareVersion,
                    'FirmwareLastUpdateDate':fac.FirmwareLastUpdateDate,
                    'DeviceEnabled': fac.DeviceEnabled,
                    'DeviceMode':fac.DeviceMode,
                    'NetworkMode':fac.NetworkMode,
                    'LastCO2Value':fac.LastCO2Value,
                    'InUse':fac.InUse,
                    'NightModeEnabled':fac.NightModeEnabled,
                    'NightModeAuto': fac.NightModeAuto,
                    'NightModeFrom': fac.NightModeFrom,
                    'NightModeTo': fac.NightModeTo,
                    'DateCreated':fac.DateCreated,
                    'DateUpdated':fac.DateUpdated,
                    'User':str(fac.User)
                    }
            return JsonResponse(resp)
        else: 
            if Facility.objects.filter(User=request.user):
                fac = Facility.objects.get(User=request.user)
                data = {
                    'ID':fac.id,
                    'UIN':fac.UIN,
                    'Name':fac.Name,
                    'Description': fac.Description,
                    'FirmwareVersion':fac.FirmwareVersion,
                    'DeviceMode':fac.DeviceMode,
                    'NetworkMode':fac.NetworkMode,
                    'LastCO2Value':fac.LastCO2Value,
                    'NightModeEnabled':fac.NightModeEnabled,
                    'NightModeAuto':fac.NightModeAuto,
                    'NightModeFrom':fac.NightModeFrom,
                    'NightModeTo':fac.NightModeTo
                }
                return JsonResponse(data)
            else:
                return HttpResponse('Facility not setted')
    else:
        return HttpResponse("Not logged in",status=401)

@require_http_methods(['PUT'])
def Connect(request):
    """
    Description: Метод подключения установки.
    Args: request - запрос с методом PUT, содержащий UIN установки.
    """
    if request.user.is_authenticated:
        if Facility.objects.filter(User=request.user):
            return HttpResponse('Alredy own facility')
        else:
            try:
                fac = Facility.objects.get(UIN=json.loads(request.body)['UIN'])
                if fac.InUse:
                    return HttpResponse('Alredy in use')
                else:
                   setattr(fac,'User',request.user)
                   setattr(fac,'InUse',True)
                   fac.save()
                   return HttpResponse('Facility connected')
            except:
                return HttpResponse('Bad request',status=400)
    else:
        return HttpResponse('Not logged in',status=401)