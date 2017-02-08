import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils import formats

from plot.models import *
from sensor.models import *

def make_timestamp( row ):
    row["timestamp_data"] = TimeStamp.create( row["timestamp_data"] )
    return row


class Quick(View):

    def get(self , request):
        device_list = Device.objects.all()

        if "time" in request.GET:
            end_time = TimeStamp.parse_datetime( request.GET["time"] )
            print "end_time: %s" % end_time
        else:
            last = RawData.objects.latest( 'timestamp_data' )
            end_time = last.timestamp_data
            
        start_time = end_time - datetime.timedelta( seconds = 14 * 24 * 3600 )
        try:
            pm10_type = MeasurementType.objects.get( name = "PM10" )
            pm25_type = MeasurementType.objects.get( name = "PM25" )
        except MeasurementType.DoesNotExist:
            return HttpResponse( "Internal error - missing measurement types PM10 / PM25" , status = 500 )
            
        data_all = RawData.objects.filter( timestamp_data__range=(start_time , end_time)).values( "id", "value", "timestamp_data", "sensor_id").order_by('timestamp_data')
        
        device_rows = []
        for d in device_list:
            if d.location is None:
                continue
                

            try:
                pm10sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = pm10_type )
                pm25sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = pm25_type )
            except Sensor.DoesNotExist:
                continue

            data25query = [x for x in data_all if x["sensor_id"] == pm25sensor.id]
            data10query = [x for x in data_all if x["sensor_id"] == pm10sensor.id]

            data25list = map( make_timestamp , data25query )
            data10list = map( make_timestamp , data10query )
            
            if len(data25list) == 0:
                continue

            time = data25list[-1]["timestamp_data"]

            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'pm25': data25list[0]["value"],
                'pm10': data10list[0]["value"],
                'pm25list': data25list, 
                'pm10list': data10list,
                'time': time}
            device_rows.append(row)

        json_string = json.dumps(device_rows)

        context = {"device_rows" : device_rows, 
                   "date": end_time, 
                   "device_json": json_string, 
                   "timestamp": str(end_time) }

        return render( request , "friskby/quick.html" , context )
