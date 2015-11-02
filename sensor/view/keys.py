from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import View

from api_key.models import *

class KeyView(View):


    @method_decorator(login_required)
    def dispatch(self , *args, **kwargs):
        return super(KeyView, self).dispatch(*args, **kwargs)

        
    def get(self , request):
        context = {"keys" : ApiKey.objects.all() }
        return render( request , "sensor/keys/overview.html" , context )
        





        

