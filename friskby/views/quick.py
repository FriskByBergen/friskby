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
        else:
            last = RawData.objects.latest( 'timestamp_data' )
            end_time = last.timestamp_data

        if "start" in request.GET:
            start_time = TimeStamp.parse_datetime( request.GET["start"] )
            print(start_time)
        else:
            start_time = end_time - datetime.timedelta( seconds = period )

        if "sensortype" in request.GET:
            sensor_type_name = request.GET["sensortype"]
        else:
            sensor_type_name = "PM10"

        if sensor_type_name == "PM10":
            other_sensor_name = "PM25"
        else:
            other_sensor_name = "PM10"

        previous_start = start_time - (end_time - start_time)
        previous_end = start_time

        next_start = end_time
        next_end = end_time + (end_time - start_time)

        try:
            sensortype = MeasurementType.objects.get( name = sensor_type_name )
        except MeasurementType.DoesNotExist:
            return HttpResponse( "Internal error - missing measurement type %s" % sensortype , status = 500 )
            
        data_all = RawData.objects.filter( timestamp_data__range=(start_time , end_time)).values( "id", "value", "timestamp_data", "sensor_id").order_by('timestamp_data')

        algo_start = dt.now()
        device_rows = []
        for d in device_list:
            if d.location is None:
                continue
                
            try:
                sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = sensortype )
            except Sensor.DoesNotExist:
                continue

            dataquery = downsample([x for x in data_all if x["sensor_id"] == sensor.sensor_id], minutes=30, cutoff=100)

            datalist = map( make_timestamp , dataquery )
            
            if len(datalist) == 0:
                continue

            time = datalist[-1]["timestamp_data"]
            time_pp = dt_parser.parse(time).strftime('%b. %d, %H:%M') # %d-%m-%Y %H:%M
            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'pm25': datalist[0]["value"],
                'pm10': datalist[0]["value"],
                'datalist': datalist,
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
                   "timestamp": end_time,
                   "current_start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "current_end": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "previous_start": previous_start.strftime("%Y-%m-%d %H:%M:%S"),
                   "previous_end": previous_end.strftime("%Y-%m-%d %H:%M:%S"),
                   "next_start": next_start.strftime("%Y-%m-%d %H:%M:%S"),
                   "next_end": next_end.strftime("%Y-%m-%d %H:%M:%S"),
                   "sensortype": sensor_type_name,
                   "othersensor": other_sensor_name}

        return render( request , "friskby/quick.html" , context )
