from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Adm(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Adm, self).dispatch(*args, **kwargs)
        
        
    def get(self , request):
        return render( request , "friskby/adm.html" )
