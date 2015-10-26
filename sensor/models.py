from django.utils import dateparse
from django.db.models import *
from django.core.validators import RegexValidator


class DataType( Model ):
    id = CharField("DataType" , max_length = 60 , primary_key = True)

    def __unicode__(self):
        return self.id


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
    # When parsing a string the format should be as: "2015-10-10T10:10:00+01";
    # i.e. yyyy-mm-ddTHH:MM:SS+zz
    # Where the +zz is a timezone shift relative to UTC; i.e. +01 for Central European Time.

    timestamp = DateTimeField("timestamp")

    def __unicode__(self):
        return str(self.timestamp)


    @classmethod
    # This takes a time_string which is supposed to be in the time
    # zone given by the settings.TIME_ZONE variable. The resulting
    # dt variable is a time zone aware datetime instance.
    def parse_datetime(cls , time_string ):
        dt = dateparse.parse_datetime( time_string )
        return dt


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




class DataInfo( Model ):
    location = ForeignKey( Location )
    timestamp = ForeignKey( TimeStamp )
    sensor = ForeignKey( SensorID )

    
    def __unicode__(self):
        return "%s @ %s" % ( self.sensor , self.timestamp )

    
    def save(self , *args, **kwargs):
        # If the sensor indeed has a location you should not supply an
        # extra location with the DataInfo() object. In case you the
        # location from the sensor will override anyway.
        if not self.sensor.location is None:
            self.location = self.sensor.location
        super(DataInfo , self).save(*args , **kwargs)
