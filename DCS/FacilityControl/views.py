from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .models import Facility
from string import ascii_letters,digits
from django.utils import timezone
from random import choices


# Create your views here.
@require_http_methods(['POST'])
def Create(request):
    if request.user.is_authenticated:
        if not request.user.IsAdmin:
            AllDigits = ascii_letters+digits
            UIN ='zCO2-'+''.join(choices(AllDigits, k=12))
            timezone.activate("Europe/Moscow")
            now = timezone.now()
            facility = Facility(
                UIN=UIN,Name=request.POST.get('Name'),
                Description=request.POST.get('Description'),
                DateCreated=now,
                DateUpdated=now
                )
            facility.SNumber = request.POST.get('SNum')
            facility.FVer =request.POST.get('FVer')
            facility.FLastUpdate = now
            facility.save()
            return HttpResponse("Created",status=201)
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)