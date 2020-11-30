from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json

from .models import Log
from FacilityControl.models import Facility
# Create your views here.
@require_http_methods(['POST'])
def Create(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        if request.user.facility.id == data['id']:
            timezone.activate("Europe/Moscow")
            Log(Facility=Facility.objects.get(id = data['id']),LogContent=data['LogContent'],LogDate=timezone.now()).save()
            return HttpResponse('Created',status=201)
        else:
            return HttpResponse('Not your facility', status=400)
    else:
        return HttpResponse('Not logged in',status=401)

@require_http_methods(['GET'])
def View(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            logs = Log.objects.filter(Facility=Facility.objects.get(id=data['id']))
            paginator = Paginator(logs,15)
            try:
                page = paginator.page(data['page'])
            except PageNotAnInteger:
                return HttpResponse("Page not an integer",status=400)
            except EmptyPage:
                return HttpResponse("Empty page",status=400)
            if len(page.object_list)>1:
                resp={}
                for log in page.object_list:
                    resp['Log_'+str(log.id)]={
                        'LogContent':log.LogContent,
                        'LogDate': log.LogDate
                        }
                return JsonResponse(resp)
            else:
                return HttpResponse('No logs')
        else: 
            if request.user.facility.id == data['id']:
                logs = Log.objects.filter(Facility=Facility.objects.get(id=data['id']))
                paginator = Paginator(logs,15)
                try:
                    page = paginator.page(data['page'])
                except PageNotAnInteger:
                    return HttpResponse("Page not an integer",status=400)
                except EmptyPage:
                    return HttpResponse("Empty page",status=400)
                if len(page.object_list)>1:
                    resp={}
                    for log in page.object_list:
                        resp['Log_'+str(log.id)]={
                            'LogContent':log.LogContent,
                            'LogDate': log.LogDate
                            }
                    return JsonResponse(resp)
                else:
                    return HttpResponse("No logs")
            else:
                return HttpResponse('Not your facility',status=400)
    else:
        return HttpResponse("Not logged in",status=401)

@require_http_methods(['DELETE'])
def Delete(request):
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            Log.objects.filter(Facility=Facility.objects.get(id=json.loads(request.body)['id'])).delete()
            return HttpResponse("Deleted")
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)