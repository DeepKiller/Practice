from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
# Create your models here.
class User(AbstractBaseUser):
    password=None
    Email = models.EmailField(name="Email",max_length=254,null=False)
    Password = models.CharField(name="Password",max_length=254,null=False)
    IsConfirmed = models.BooleanField(name="IsConfimed",null=False,default=False)
    Roles = (('Admin','Admin'),('User','User'))
    Role = models.CharField(name='Role',max_length=20,null=False,choices=Roles,default="User")
    DateCreated = models.DateField(name='DateCreated',null=False)
    DateUpdated = models.DateField(name='DateUpdated',null=False)
