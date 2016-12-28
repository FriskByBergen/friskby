from django.shortcuts import render
from django.views.generic import View


class MainView(View):

    def get(self , request):
        return render( request , "sensor/main.html" )




