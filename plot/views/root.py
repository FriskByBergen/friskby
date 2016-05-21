from django.shortcuts import render
from django.views.generic import View


class Root(View):
    
    def get(self , request):
        return render( request , "plot/root.html" )
