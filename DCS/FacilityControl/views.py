from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .models import Facility
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