from django.urls import path
from LogControl import views

urlpatterns = [
    path('create',views.Create),
    path('view',views.View),
    path('delete',views.Delete)
]
