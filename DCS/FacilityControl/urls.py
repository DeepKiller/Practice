from django.urls import path
from FacilityControl import views

urlpatterns = [
    path('create', views.Create),
    path('delete',views.Delete),
]