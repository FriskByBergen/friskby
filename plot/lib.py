import math
import plotly.offline
from plotly.graph_objs import Scatter

default_kwargs = {"output_type" : "div"}

def test():
    x = [ math.pi*2*x/100 for x in range(100) ]
    y = [ math.sin(arg) for arg in x ]
    data = [ Scatter(x=x , y = y)]
    
    return plotly.offline.plot( {"data" : data } , **default_kwargs )
    

