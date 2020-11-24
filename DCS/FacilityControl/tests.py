from django.test import TestCase, Client
from django.http import HttpRequest
# Create your tests here.
class Testing(TestCase):
    def CreateTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/login',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/facilitycontrol/create',{'Name':'TEST','Description':'TEST','SNum':'NTST','FVer':'11.0'})
        if response.status_code != 201:
            self.fail(response.content)