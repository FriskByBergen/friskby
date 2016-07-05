from datetime import timedelta
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
    pair = sensor.get_vectors( )
    if pair:
        ts , values = pair
        df = pd.DataFrame().from_dict({"ts" : ts , "values" : values})
        df.index = df['ts']

        df.index = df.index + timedelta(hours=2)
        df = df.resample('10Min')
        
        label = "%s : %s" % (sensor.parent_device.id , sensor.sensor_type)
        return Scatter( x=df.index,
                        y=df['values'],
                        name=label)
    else:
        return None


def trace_plot(sensor_list):
    data = []
    for sensor in sensor_list:
        trace = get_trace( sensor )
        if trace:
            data.append( trace )

    if data:
        return plotly.offline.plot( {"data" : data }, **default_kwargs )
    else:
        return None




def trace_plot_FriskPI():
    DEVICEIDS = ["FriskPI01","FriskPI02","FriskPI03","FriskPI04","FriskPI05","FriskPI06",
                 "BG_1","BG_2","BG_3","BG_4"]

    sensor_list = []
    for dev_id in DEVICEIDS:
        for pm in ["PM10" , "PM25"]:
            sensor_id = "%s_%s" % (dev_id , pm)

            try:
                sensor_list.append( Sensor.objects.get( pk = sensor_id ) )
            except Sensor.DoesNotExist:
                pass
        
    return trace_plot( sensor_list )


