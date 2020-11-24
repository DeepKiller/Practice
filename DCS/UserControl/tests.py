from django.test import TestCase, Client
from django.http import HttpRequest

# Create your tests here.
class Testing(TestCase):
    def RegTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'b@b.b','Password':'NcafBfdnsB2'})
        if response.status_code==200:
            self.fail(response.content)
    
    def LogTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/login',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        if not response.status_code==200:
            self.fail(response.content)
    
    def DelTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/login',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.delete('/usercontrol/delete',{'Email':'a@a.a'})
        if not response.status_code==200:
            self.fail(response.content)
    
    def GetTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/registration',{'Email':'b@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/registration',{'Email':'c@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/registration',{'Email':'d@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.post('/usercontrol/login',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        response = test.get('/usercontrol/view',{'page':'1'})
        if not response.status_code==200:
            self.fail(response.content)
        else:
            print(response.content)