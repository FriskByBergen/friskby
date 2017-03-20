import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils import formats

from datetime import timedelta
import dateutil.parser

from sensor.models import *
import numpy as np

def make_timestamp(row):
    timedate_format = "%Y-%m-%dT%H:%M:%SZ"
    row["timestamp_data"] = TimeStamp.create(row["timestamp_data"], timedate_format)
    return row

class Median(View):

    def get(self, request):
        period = 2 * 24 * 3600 # 2 days
        delta_minutes = 60 # sample every 60 minutes
        device_list = Device.objects.all()
        default_sensors = ('FriskPaiMorten', 'FriskPI05', 'FriskPI06',
                           'FriskPI09', 'FriskPI10', 'FriskPIFlikka',
                           'FriskPiSasak')

        if 'delta' in request.GET:
            try:
                delta_minutes = int(request.GET["delta"])
            except ValueError as err:
                print('Received non int as delta: %s' % err)
        delta = timedelta(minutes=delta_minutes)

        if "end" in request.GET:
            end_time = TimeStamp.parse_datetime(request.GET["end"])
        else:
            last = RawData.objects.latest('timestamp_data')
            end_time = last.timestamp_data

        start_time = None
        if "start" in request.GET:
            start_time = TimeStamp.parse_datetime(request.GET["start"])
        if not start_time:
            start_time = end_time - datetime.timedelta(seconds=period)
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

        if "sensortype" in request.GET:
            sensor_type_name = request.GET["sensortype"]
        else:
            sensor_type_name = "PM10"

        try:
            sensortype = MeasurementType.objects.get(name=sensor_type_name)
        except MeasurementType.DoesNotExist:
            return HttpResponse("Internal error - missing measurement type %s" % sensor_type_name, status=500)

        data_all = RawData.objects.filter(timestamp_data__range=(start_time,
            end_time)).values('s_id',
                              'value',
                              'timestamp_data').order_by('timestamp_data')

        algo_start = TimeStamp.now()
        device_rows = []
        for d in device_list:
            try:
                if not d.location or d.id not in default_sensors:
                    continue
                sensor = Sensor.objects.get(parent_device=d,
                                            sensor_type__measurement_type=sensortype)
            except Sensor.DoesNotExist:
                continue

            dataquery = [x for x in data_all if x['s_id'] == sensor.s_id]
            datalist = map(make_timestamp, dataquery)

            if len(datalist) == 0:
                continue

            row = {
                'id': d.id,
                'locname': d.location.name,
                'datalist': datalist
            }
            device_rows.append(row)

        the_data = {}
        for row in device_rows:
            idx = 0
            datalist = row['datalist']
            now_time = start_time
            while now_time < end_time:
                current_measurements = []
                val = lambda i: datalist[i]['value']
                ts  = lambda i: dateutil.parser.parse(datalist[i]['timestamp_data'])
                while ts(idx) < now_time and idx < len(datalist)-1:
                    current_measurements.append(val(idx))
                    idx += 1
                if not now_time in the_data:
                    the_data[now_time] = []
                the_data[now_time] += current_measurements
                now_time = now_time + delta

        mean_values = []
        std_values  = []
        for sometime in the_data:
            vals = np.array(sorted(the_data[sometime]))
            if len(vals) > 2:
                percentile_10 = max(1, len(vals)//10) # remove top and bottom 10%
                vals = vals[percentile_10:-percentile_10]
                mean_values.append({'timestamp_data':sometime.isoformat(),
                                    'value':round(vals.mean(), 2)})
                std_values.append({'timestamp_data':sometime.isoformat(),
                                    'value':round(vals.std(), 2)})

        mean_values.sort(key=lambda x:x['timestamp_data'])
        std_values.sort(key=lambda x:x['timestamp_data'])

        algo_end = TimeStamp.now()
        algo_delta = algo_end - algo_start
        print('total time used: %.2f sec' % algo_delta.total_seconds())
        json_string = json.dumps(device_rows)

        context = {"device_json": json_string,
                   "timezone_offset": TimeStamp.timezoneOffset(),
                   'start_time': start_time.strftime('Bergen air quality trend since %B %d.'),
                   'meandata': mean_values,
                   'stddata': std_values
        }

        return render(request, "friskby/median.html", context)
