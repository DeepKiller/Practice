from django.test import TestCase, Client

# Create your tests here.
class Testing(TestCase):
    def RegTest(self):
        test = Client()
        response = test.post('/usercontrol/registration',{'Email':'a@a.a','Password':'aaaaaaaaa'})
        if response.status_code==200:
            self.fail(response.content)
    
    def LogTest(self):
        test = Client()
        response = test.post('/usercontrol/login',{'Email':'a@a.a','Password':'CpRm9Cg8mNSFzFt'})
        if response.status_code==200:
            self.fail(response.content)