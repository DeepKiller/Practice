from django.db import models
from FacilityControl.models import Facility

class Log(models.Model):
    LogContent = models.CharField(name="LogContent",max_length=254,null=False)
    LogDate = models.DateField(name="LogDate",null=False)
    Facility = models.ForeignKey(Facility,name="Facility",to_field='UIN',null=False,on_delete=models.DO_NOTHING)