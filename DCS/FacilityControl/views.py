from django.core import serializers
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse,JsonResponse
from .models import Facility
from UserControl.models import User
from string import ascii_letters,digits
from django.utils import timezone
from random import choices
import json

# Create your views here.
@require_http_methods(['POST'])
def Create(request):
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            data = json.loads(request.body)
            AllDigits = ascii_letters+digits
            UIN ='zCO2-'+''.join(choices(AllDigits, k=12))
            timezone.activate("Europe/Moscow")
            now = timezone.now()
            facility = Facility(
                UIN=UIN,Name=data['Name'],
                Description=data['Description'],
                SerialNumber=data['SNum'],
                FirmwareVersion=data['FVer'],
                FirmwareLastUpdateDate=now,
                DateCreated=now,
                DateUpdated=now
                )
            facility.save()
            return HttpResponse("Created",status=201)
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['DELETE'])
def Delete(request):
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            data = json.loads(request.body)
            Facility.objects.get(id=data['id']).delete()
            return HttpResponse("Deleted")
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['PUT'])
def Change(request):
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            timezone.activate("Europe/Moscow")
            now = timezone.now()
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
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)

@require_http_methods(['GET'])
def View(request):
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
            return HttpResponse("No permision",status=403)
    else:
        return HttpResponse("Not logged in",status=401)

@require_http_methods(['PUT'])
def Connect(request):
    if request.user.is_authenticated:
        if Facility.objects.filter(User=request.user):
            return HttpResponse('Alredy own facility')
        else:
            fac = Facility.objects.get(UIN=json.loads(request.body)['UIN'])
            if fac.InUse:
                return HttpResponse('Alredy in use')
            else:
               setattr(fac,'User',request.user)
               setattr(fac,'InUse',True)
               fac.save()
               return HttpResponse('Facility connected')
    else:
        return HttpResponse('Not logged in',status=401)