from django.shortcuts import render
from django.views.generic import View

from plot.models import *

import sensor.models as models

def get_current_timestamp():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT CURRENT_TIMESTAMP")
    rows = cursor.fetchone()
    return rows[0]

class Quick(View):

    def get(self , request):
        device_list = models.Device.objects.all()

        current_time = request.GET.get('time', get_current_timestamp())

        device_rows = []
        for d in device_list:
            pm25sensor = next(x for x in d.sensorList() if x.description == "PM25")
            pm10sensor = next(x for x in d.sensorList() if x.description == "PM10")
            dataSql = """
            SELECT * FROM sensor_rawdata
            where sensor_id = '%s' and timestamp_recieved < '%s'
            order by timestamp_recieved asc LIMIT 1"""
            data25 = models.RawData.objects.raw(dataSql % (pm25sensor.id, current_time))[0]
            data10 = models.RawData.objects.raw(dataSql % (pm10sensor.id, current_time))[0]

            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'pm25': data25.value,
                'pm10': data10.value,
                'time': data25.timestamp_recieved }
            device_rows.append(row)
            print(vars(d))
            print(row)

        context = {"device_rows" : device_rows }
        return render( request , "friskby/quick.html" , context )
