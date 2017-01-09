from django.shortcuts import render
from django.views.generic import View

from plot.models import *

import sensor.models as models

def get_current_timestamp():
    from django.db import connection
    cursor = connection.cursor()
    # use this for debug
    cursor.execute("SELECT timestamp_data from sensor_rawdata order by timestamp_data desc limit 1")
    #cursor.execute("SELECT CURRENT_TIMESTAMP")
    rows = cursor.fetchone()
    return rows[0]

class Quick(View):

    def get(self , request):
        import json
        from django.utils import formats
        device_list = models.Device.objects.all()

        current_time = request.GET.get('time', get_current_timestamp())
        print(current_time)
        device_rows = []
        for d in device_list:
            pm25sensor = next(x for x in d.sensorList() if x.description == "PM25")
            pm10sensor = next(x for x in d.sensorList() if x.description == "PM10")
            dataSql = """
            SELECT id, value, timestamp_data FROM sensor_rawdata
            where sensor_id = '%s'
              and timestamp_data <= '%s'
              and timestamp_data > TIMESTAMP '%s' - INTERVAL '2 weeks'
            order by timestamp_data asc"""
            data25 = models.RawData.objects.raw(dataSql % (pm25sensor.id, current_time, current_time))
            data10 = models.RawData.objects.raw(dataSql % (pm10sensor.id, current_time, current_time))
            data25list = list({"value": x.value, "id": x.id, "timestamp": str(x.timestamp_data)} for x in data25)
            data10list = list({"value": x.value, "id": x.id, "timestamp": str(x.timestamp_data)} for x in data10)
            time = formats.date_format(data25[0].timestamp_data, "d/m-f")
            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'pm25': data25[0].value,
                'pm10': data10[0].value,
                'pm25list': data25list,
                'pm10list': data10list,
                'time': time }
            device_rows.append(row)
            print(vars(d))
            print(row)

        json = json.dumps(device_rows)

        context = {"device_rows" : device_rows, "date": current_time, "device_json": json, "timestamp": str(current_time) }
        return render( request , "friskby/quick.html" , context )
