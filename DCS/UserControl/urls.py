from django.urls import path
from UserControl import views

urlpatterns = [
    path('registration', views.Registration),
    path('login',views.Login)
]