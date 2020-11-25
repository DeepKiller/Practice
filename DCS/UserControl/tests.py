from django.test import TestCase, Client
from django.http import HttpRequest
import json

# Create your tests here.
class Testing(TestCase):
    def RegTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',json.dumps({'Email':'b@b.b','Password':'NcafBfdnsB2'}),content_type='application/json')
        if response.status_code==200:
            self.fail(response.content)
    
    def LogTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',json.dumps({'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        response = test.post('/usercontrol/login',json.dumps({'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        if not response.status_code==200:
            self.fail(response.content)
    
    def DelTest(self):
        test = Client()
        info=json.dumps({'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        dele = json.dumps({'Email':'a@a.a'})
        response = test.post('/usercontrol/registration',info,content_type='application/json')
        response = test.post('/usercontrol/login',info,content_type='application/json')
        response = test.delete('/usercontrol/delete',dele,content_type='application/json')
        if not response.status_code==200:
            self.fail(response.content)
    
    def GetTest(self):
        test = Client()
        
        response = test.post('/usercontrol/registration',json.dumps({'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        response = test.post('/usercontrol/registration',json.dumps({'Email':'b@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        response = test.post('/usercontrol/registration',json.dumps({'Email':'c@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        response = test.post('/usercontrol/registration',json.dumps({'Email':'d@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        response = test.post('/usercontrol/login',json.dumps({'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'}),content_type='application/json')
        pg = json.dumps({'page':'1'})
        response = test.get('/usercontrol/view',{'page':1})
        if not response.status_code==200:
            self.fail(response.content)
        else:
            print(response.content)