from django.db import models

# Create your models here.
class Facility(models.Model):
    UIN = models.CharField(name="UIN",max_length=17,null=False,unique=True)
    Name = models.CharField(name="Name",max_length=254)
    Description = models.CharField(name="Description",max_length=254)
    SNumber = models.CharField(name="SerialNumber",max_length=254,null=False)
    FVer = models.CharField(name="FirmwareVersion",null=False,max_length=254)
    FLastUpdate = models.DateField(name="FirmwareLastUpdateDate",null=False)
    DeviceEnabled = models.BooleanField(name="DeviceEnabled",null=False, default=False)
    DeviceModes = [('off','Off'),('one','One'),('two','Two'),('three','Three'),('four','Four')]
    DeviceMode = models.CharField(name="DeviceMode",null=False,choices=DeviceModes,max_length=254,default=DeviceModes[0][1])
    NetworkModes = [('home','Home'),('OneDevice','OneDevice')]
    NetworkMode = models.CharField(name="NetworkMode",null=False,choices=NetworkModes,max_length=254)
    LastCO2 = models.DecimalField(name="LastCO2Value",max_digits=5, decimal_places=2,null=True)
    InUse = models.BooleanField(name="InUse", null=False, default=False)
    NightModeEnabled = models.BooleanField(name="NightModeEnabled", null=False,default=False)
    NightModeAuto = models.BooleanField(name="NightModeAuto", null=False,default=False)
    NightModeFrom = models.TimeField(name="NightModeFrom",null=True)
    NightModeTo = models.TimeField(name="NightModeTo",null=True)
    DateCreated = models.DateField(name='DateCreated',null=False)
    DateUpdated = models.DateField(name='DateUpdated',null=False)

    def __str__(self):
        return self.Name
