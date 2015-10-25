from django.db.models import *
from django.core.validators import RegexValidator


class DataType( Model ):
    id = CharField("DataType" , max_length = 60 , primary_key = True)
    

class Company( Model ):
    name = CharField("Device manufacturer" , max_length = 60)

    def __unicode__(self):
        return self.name


class DeviceType( Model ):
    name = CharField("Name of the device" , max_length = 60 )
    company = ForeignKey( Company )

    def __unicode__(self):
        return self.name


class MeasurementType( Model ):
    name = CharField("Type of measurement" , max_length = 60)
    
    def __unicode__(self):
        return self.name


class TimeStamp( Model ):
    timestamp = DateTimeField("timestamp")


class Location( Model ):
    name = CharField("Location" , max_length = 60 )
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    altitude = FloatField("Altitude" , null = True)

    def __unicode__(self):
        return self.name
        

class SensorID( Model ):
    IDPattern = "[-_:a-zA-Z0-9]+"

    id = CharField("Sensor ID" , max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    location = ForeignKey( Location , null = True )
    parent_device = ForeignKey( DeviceType )
    measurement_type = ForeignKey( MeasurementType )
    data_type = ForeignKey( DataType , default = "TEST" )
    description = CharField("Description" , max_length = 256 )
    unit = CharField("Unit" , max_length = 60 )
    min_value = FloatField("Minimum value")
    max_value = FloatField("Maximum value")
    

    def __unicode__(self):
        return self.id


    def valid_input(self , value):
        if not isinstance(value,float):
            try:
                value = float(value)
            except:
                return False
                
        if self.min_value <= value <= self.max_value:
            return True

        return False




