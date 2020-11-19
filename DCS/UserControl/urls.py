from django.urls import path
from UserControl import views

urlpatterns = [
    path('', views.Registration)
]