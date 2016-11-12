from sensor.models import *

def sensor_list( options ):
    if options["sensor"]:
        return [ Sensor.objects.get( pk = options["sensor"] ) ]
    else:
        if options["device"]:
            dev_list = [ Device.objects.get( pk = options["device"] )]
        else:
            dev_list = Device.objects.all()
            
        sensor_list = []
        for dev in dev_list:
            for sensor in dev.sensorList():
                sensor_list.append( sensor )
        
        return sensor_list
