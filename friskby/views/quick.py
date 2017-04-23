import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils import formats

from sensor.models import *
from sensor.sample import make_datalist

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
        else:
            start_time = end_time - datetime.timedelta( seconds = period )

        if "sensortype" in request.GET:
            sensor_type_name = request.GET["sensortype"]
        else:
            sensor_type_name = "PM10"

        if sensor_type_name == "PM10":
            other_sensor_name = "PM25"
            pretty_sensor = u'10 \u00b5m'
            pretty_other = u'25 \u00b5m'
        else:
            other_sensor_name = "PM10"
            pretty_sensor = u'25 \u00b5m'
            pretty_other = u'10 \u00b5m'

        previous_start = start_time - (end_time - start_time)
        previous_end = start_time

        next_start = end_time
        next_end = end_time + (end_time - start_time)

        try:
            sensortype = MeasurementType.objects.get( name = sensor_type_name )
        except MeasurementType.DoesNotExist:
            return HttpResponse( "Internal error - missing measurement type %s" % sensor_type_name , status = 500 )
            
        data_all = RawData.objects.filter(timestamp_data__range=(start_time,
            end_time)).values('sensor',
                              'value',
                              'timestamp_data').order_by('timestamp_data')

        algo_start = TimeStamp.now()
        device_rows = []
        for d in device_list:
            if d.location is None:
                continue
                
            try:
                sensor = Sensor.objects.get( parent_device=d, sensor_type__measurement_type = sensortype )
            except Sensor.DoesNotExist:
                continue

            datalist = make_datalist( [x for x in data_all if x['sensor'] == sensor.s_id], block_size = 30, value_cutoff=100)
            if len(datalist) == 0:
                continue

            time = datalist[-1]["timestamp_data"]
           
            time_pp = TimeStamp.create(TimeStamp.parse_datetime(time), '%b. %d, %H:%M', True) 

            row = {
                'id': d.id,
                'locname': d.location.name,
                'lat': d.location.latitude,
                'long': d.location.longitude,
                'last': datalist[-1]["value"],
                'datalist': datalist,
                'time': time_pp,
                'isotime': time}
            device_rows.append(row)

        # this sorts the devices lexicographically, but BG_XXX devices last
        cmp_ln = lambda x: x['locname']
        cmp_id = lambda x: 1 if x['id'][:2] == 'BG' else 0
        device_rows = sorted(device_rows, key=cmp_ln)
        device_rows = sorted(device_rows, key=cmp_id)

        algo_end = TimeStamp.now()
        algo_delta = algo_end - algo_start
        print('total time used: %.2f sec' % algo_delta.total_seconds())
        json_string = json.dumps(device_rows)

        context = {"device_rows" : device_rows, 
                   "date": end_time, 
                   "device_json": json_string, 
                   "timestamp": end_time,
                   "timezone_offset": TimeStamp.timezoneOffset(),
                   "current_start": TimeStamp.create(start_time, "%Y-%m-%dT%H:%M:%S"),
                   "current_end": TimeStamp.create(end_time, "%Y-%m-%dT%H:%M:%S"),
                   "previous_start": TimeStamp.create(previous_start, "%Y-%m-%dT%H:%M:%S"),
                   "previous_end": TimeStamp.create(previous_end, "%Y-%m-%dT%H:%M:%S"),
                   "next_start": TimeStamp.create(next_start, "%Y-%m-%dT%H:%M:%S"),
                   "next_end": TimeStamp.create(next_end, "%Y-%m-%dT%H:%M:%S"),
                   "sensortype": sensor_type_name,
                   "othersensor": other_sensor_name,
                   "pretty_sensor": pretty_sensor,
                   "pretty_other": pretty_other}

        return render( request , "friskby/quick.html" , context )
