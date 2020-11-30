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
    """
    Description: Создаёт новый лог из полученных данных.
    Args:  request - запрос от клиента с методом POST содержащий в себе id установки и LogContent - содержимое лога.
    """
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
    """
    Description: Отображает список логов на указанной странице. Для администратора для запрошенной установки, для пользователя для привязанной.
    Args: request - запрос от клиента с методом GET содержащий в себе page (номер необходимой страницы).
    """
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
    """
    Description: Удаляет логи с помощью полученных в запросе данных.
    Args: request - запрос от клиента с методом DELETE содержащий в себе id установки для удаления логов.
    """
    if request.user.is_authenticated:
        if request.user.IsAdmin:
            Log.objects.filter(Facility=Facility.objects.get(id=json.loads(request.body)['id'])).delete()
            return HttpResponse("Deleted")
        else: 
            return HttpResponse("No permision", status=403)
    else:
        return HttpResponse("Not logged in", status=401)