from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def get_by_natural_key(self,username):
        return User.objects.filter(Email=username)
    def create_user(self,Email,Password):
        timezone.activate("Europe/Moscow")
        user=self.model(Email=Email,Password=Password,DateCreated=timezone.now(),DateUpdated=timezone.now())
        user.save()
        return user

class User(AbstractBaseUser):
    Email = models.EmailField(name="Email",max_length=254,null=False,unique=True)
    Password = models.CharField(name="Password",max_length=254,null=False)
    IsConfirmed = models.BooleanField(name="IsConfimed",null=False,default=False)
    Roles = (('Admin','Admin'),('User','User'))
    Role = models.CharField(name='Role',max_length=20,null=False,choices=Roles,default="User")
    DateCreated = models.DateField(name='DateCreated',null=False)
    DateUpdated = models.DateField(name='DateUpdated',null=False)
    last_login=None
    password=None
    USERNAME_FIELD = 'Email'
    objects = UserManager()

    def __str__(self):
        return self.Email
        
    @property
    def IsAdmin(self):
        if self.Role == "Admin":
            return True
        return False


