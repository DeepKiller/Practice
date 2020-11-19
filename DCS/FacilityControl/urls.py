from django.urls import path
from FacilityControl import views

urlpatterns = [
    path('', views.Create)
]