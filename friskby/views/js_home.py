from django.shortcuts import render
from django.views.generic import View


class JSHome(View):
    
    def get(self , request):
        context = { }
        return render( request , "friskby/index.html" , context )
