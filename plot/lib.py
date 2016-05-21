import math
import pandas as pd
import plotly.plotly as py
import plotly.tools as tls
import plotly.offline
from   plotly.graph_objs import Scatter

from sensor.models import *


default_kwargs = {"output_type" : "div", 
                  "include_plotlyjs" : False,
                  "show_link" : False }


def test():
    x = [ math.pi*2*x/100 for x in range(100) ]
    y = [ math.sin(arg) for arg in x ]
    data = [ Scatter(x=x , y = y)]
    
    return plotly.offline.plot( {"data" : data } , **default_kwargs )
    


def get_trace(sensor):    
    ts,values = sensor.get_vectors( )
    datadict = []
    if len(ts) > 0:
        df = pd.DataFrame().from_dict({"ts" : ts , "values" : values})
        df = pd.DataFrame(datadict)
        df['time'] = pd.to_datetime(df['ts'])
        df.index = df['time']

        df.index = df.index + timedelta(hours=2)
        df = df.resample('10Min')
        
        label = "%s : %s" % (sensor.parent_device.id , sensor.sensor_type)
        return Scatter( x=df.index,
                        y=df['values'],
                        name=label)
    else:
        return None


def trace_plot():
    return test()
    #or sensor in Sensor.objects.all():
    #   if sensor.on_line:

    DEVICEIDS = ["FriskPI01","FriskPI02","FriskPI03","FriskPI04","FriskPI05"]
    sensor_list = []
    for dev_id in DEVICEIDS:
        for pm in ["PM10" , "PM25"]:
            sensor_id = "%s_%s" % (dev_id , pm)

            try:
                sensor_list.append( Sensor.objects.get( pk = sensor_id ) )
            except Sensor.DoesNotExist:
                pass
        
    data = []
    for sensor in sensor_list:
        trace = get_trace( sensor )
        if trace:
            data.append( trace )

    if data:
        return plotly.offline.plot( {"data" : data }, **default_kwargs )
    else:
        return None

