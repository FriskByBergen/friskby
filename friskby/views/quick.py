import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils import formats

from dateutil import parser as dt_parser
from datetime import datetime as dt

from plot.models import *
from sensor.models import *

def make_timestamp( row ):
    row["timestamp_data"] = TimeStamp.create( row["timestamp_data"] )
    return row

def with_cutoff(elt, cutoff):
    elt['value'] = min(cutoff, elt['value'])
    return elt

def downsample(lst, minutes = 15, cutoff = 100):
    if not lst:
        return []
    ret = []
    prev = None
    ret.append(with_cutoff(lst[0], cutoff))
    prev = lst[0]['timestamp_data']
    for e in lst:
        delta = e['timestamp_data'] - prev
        if delta.total_seconds() > minutes*60:
            ret.append(with_cutoff(e, cutoff))
            prev = e['timestamp_data']
    if ret[-1]['timestamp_data'] != lst[-1]['timestamp_data']:
        ret.append(with_cutoff(lst[-1], cutoff)) # retain the last element
    return ret

class Quick(View):

    def get(self , request):
        period = 7 * 24 * 3600 # 1 week
        device_list = Device.objects.all()

        if "time" in request.GET:
            end_time = TimeStamp.parse_datetime( request.GET["time"] )
            print "end_time: %s" % end_time
        else:
            last = RawData.objects.latest( 'timestamp_data' )
            end_time = last.timestamp_data
            
        start_time = end_time - datetime.timedelta( seconds = period )
        try:
            pm10_type = MeasurementType.objects.get( name = "PM10" )
            pm25_type = MeasurementType.objects.get( name = "PM25" )
        except MeasurementType.DoesNotExist:
            return HttpResponse( "Internal error - missing measurement types PM10 / PM25" , status = 500 )
            
        data_all = RawData.objects.filter( timestamp_data__range=(start_time , end_time)).values( "id", "value", "timestamp_data", "sensor_id").order_by('timestamp_data')

        algo_start = dt.now()
        device_rows = []
        for d in device_list:
            if d.location is None:
                continue
                

            try:
                pm10sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = pm10_type )
                pm25sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = pm25_type )
            except Sensor.DoesNotExist:
                continue

            data25query = downsample([x for x in data_all if x["sensor_id"] == pm25sensor.sensor_id], minutes=30, cutoff=100)
            data10query = downsample([x for x in data_all if x["sensor_id"] == pm10sensor.sensor_id], minutes=30, cutoff=100)

            data25list = map( make_timestamp , data25query )
            data10list = map( make_timestamp , data10query )
            
            if len(data25list) == 0:
                continue

            time = data25list[-1]["timestamp_data"]
            time_pp = dt_parser.parse(time).strftime('%b. %d, %H:%M') # %d-%m-%Y %H:%M
            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'pm25': data25list[0]["value"],
                'pm10': data10list[0]["value"],
                'pm25list': data25list, 
                'pm10list': data10list,
                'time': time_pp,
                'isotime': time}
            device_rows.append(row)

        algo_end = dt.now()
        algo_delta = algo_end - algo_start
        print('total time used: %.2f sec' % algo_delta.total_seconds())
        json_string = json.dumps(device_rows)

        context = {"device_rows" : device_rows, 
                   "date": end_time, 
                   "device_json": json_string, 
                   "timestamp": str(end_time) }

        return render( request , "friskby/quick.html" , context )
