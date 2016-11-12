import pytz
import datetime
from sensor.models import *
from ._arma import arma

tz = pytz.timezone("Europe/Oslo")


def sample(sensor , n):
    raw_data = RawData.objects.filter( sensor_id = sensor.id )
    if len(raw_data) == 0:
        start = tz.localize(datetime.datetime(2010, 1, 1))
    else:
        last = raw_data.last()
        start = last.timestamp_data
        
    ts = start
    data = arma( n )
    for d in data:
        ts += datetime.timedelta( seconds = 600 )
        rd = RawData.objects.create( apikey = sensor.parent_device.post_key.external_key , 
                                     sensor_id = sensor.id,
                                     timestamp_data = ts,
                                     value = d,
                                     status = RawData.VALID )

