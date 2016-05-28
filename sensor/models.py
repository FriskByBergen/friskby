import uuid
import json
import datetime
import pytz

from django.conf import settings
from django.utils import dateparse , timezone
from django.db.models import *
from django.core.validators import RegexValidator
from api_key.models import ApiKey


class RawData(Model):
    VALID = 0
    INVALID_KEY = 1
    FORMAT_ERROR = 2
    RANGE_ERROR = 3
    INVALID_SENSOR = 4
    SENSOR_OFFLINE = 5

    choices = ((VALID , "Valid") , 
               (INVALID_KEY , "Invalid key"),
               (FORMAT_ERROR , "Format error in value"),
               (RANGE_ERROR , "Value out of range"),
               (INVALID_SENSOR , "Invalid sensor ID"),
               (SENSOR_OFFLINE , "Sensor offline"))
    
    apikey = CharField(max_length=128)
    sensor_id = CharField(max_length=128)
    timestamp_recieved = DateTimeField(  ) 
    timestamp_data = DateTimeField( )
    string_value = CharField( max_length = 128 , null = True , blank = True)
    value = FloatField( default = -1 )
    status = IntegerField( default = VALID , choices = choices)
    processed = BooleanField( default = False )

    def __unicode__(self):
        return "Sensor:%s: Value:%s  status:%d" % (self.sensor_id , self.value , self.status)

    
    def save(self,*args, **kwargs):
        if self.timestamp_recieved is None:
            self.timestamp_recieved = datetime.datetime.now( pytz.utc )
        super(RawData , self).save(*args , **kwargs)
        

    @classmethod
    def valid_status( cls , status ):
        if status in [cls.VALID , cls.INVALID_KEY]:
            return True
        else:
            return False




    @classmethod
    def is_valid(cls , data):
        valid = True
        if data is None:
            valid = False
        
        if valid:
            for key in ["key" , "sensorid" , "value" , "timestamp"]:
                if not key in data:
                    valid = False
        
        if valid and settings.FORCE_VALID_SENSOR:
            try:
                sensor = Sensor.objects.get( pk = data["sensorid"] )
            except Sensor.DoesNotExist:
                valid = False

        if valid:
            ts = TimeStamp.parse_datetime( data["timestamp"] )
            if ts is None:
                valid = False

        if valid and settings.FORCE_VALID_KEY:
            valid = ApiKey.valid( data["key"] )

        return valid

    
    @classmethod
    def error(cls , data ):
        if data is None:
            return "Error: empty payload"
        
        missing_keys = []
        for key in ["key" , "sensorid" , "value" , "timestamp"]:
            if not key in data:
                missing_keys.append( key )
        if missing_keys:
            return "Error: missing fields in payload: %s" % missing_keys

        ts = TimeStamp.parse_datetime( data["timestamp"] )
        if ts is None:
            return "Error: invalid timestamp - expected: YYYY-MM-DDTHH:MM:SS+zz"

        if settings.FORCE_VALID_KEY:
            if not ApiKey.valid( data["key"] ):
                return "Error: invalid key"


        return None

    @classmethod
    def get_ts(cls , sensor , num = None , start = None ): 
        ts = []
        if num is None:
            if start is None:
                qs = RawData.objects.filter( sensor_id = sensor.id , status = RawData.VALID )
            else:
                qs = RawData.objects.filter( sensor_id = sensor.id , status = RawData.VALID, timestamp_data__gte = start)
        else:
            if start is None:
                qs = reversed( RawData.objects.filter( sensor_id = sensor.id , status = RawData.VALID).order_by('-timestamp_data')[:num] )
            else:
                raise ValueError("Can not supply both num and start")
            
        for entry in qs:
            ts.append( (entry.timestamp_data, entry.value) )
        return ts


    @classmethod
    def get_vectors(cls , sensor , num = None , start = None):
        pairs = cls.get_ts( sensor , num = num , start = start)
        ts = []
        values = []
        for (t,v) in pairs:
            ts.append( t )
            values.append( v )

        return ts,values




    @classmethod
    def create(cls , data):
        # If the is_valid() check passes we are guaranteed to store a
        # record in the rawdata table; however there might still be
        # (minor) problems with the data - that will be indicated by
        # the status flag.
        if cls.is_valid(data):
            sensor_id = data["sensorid"]
            string_value = str(data["value"])


            rd = RawData( apikey = data["key"],
                          sensor_id = sensor_id,
                          timestamp_data = TimeStamp.parse_datetime( data["timestamp"]))
            
            # 1: Check that the sensor_id is valid.
            try:
                sensor = Sensor.objects.get( pk = sensor_id )
            except Sensor.DoesNotExist:
                sensor = None
                rd.status = RawData.INVALID_SENSOR
                rd.string_value = string_value


            # 2,3: Check that value can be correctly parsed as float,
            #      and that the numerical value is in the allowed range.
            if rd.status == RawData.VALID:
                try:
                    value = float(string_value)
                    if not sensor.sensor_type.valid_range( value ):
                        rd.status = RawData.RANGE_ERROR
                        rd.string_value = string_value
                    else:
                        rd.value = value
                except ValueError:
                    rd.status = RawData.FORMAT_ERROR
                    rd.string_value = string_value
                    
            # 4: Check that the API key is valid.
            if rd.status == RawData.VALID:
                if not sensor.valid_post_key( data["key"] ):
                    rd.status = RawData.INVALID_KEY

            # 5: Check that sensor is online:
            if rd.status == RawData.VALID:
                if not sensor.on_line:
                    rd.status = RawData.SENSOR_OFFLINE

            rd.save()
            
            return rd
        else:
            raise ValueError("Invalid input data:%s " % data)


class Location( Model ):
    name = CharField("Location" , max_length = 60 )
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    altitude = FloatField("Altitude" , null = True)

    def __unicode__(self):
        return self.name


class DataType( Model ):
    id = CharField("DataType" , max_length = 60 , primary_key = True)

    def __unicode__(self):
        return self.id


class DeviceType( Model ):
    name = CharField("Name of the device" , max_length = 60 )
    
    def __unicode__(self):
        return self.name


class Device( Model ):
    IDPattern = "[-_:a-zA-Z0-9]+"

    id = CharField("Device ID" , max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    location = ForeignKey( Location , null = True )
    device_type = ForeignKey( DeviceType )
    description = CharField("Description" , max_length = 256 )
    post_key = ForeignKey( ApiKey )

    def __unicode__(self):
        return self.id

    def valid_post_key( self , key_string):
        return self.post_key.access( key_string )



class MeasurementType( Model ):
    name = CharField("Type of measurement" , max_length = 60)
    
    def __unicode__(self):
        return self.name


class TimeStamp( Model ):
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
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

    @classmethod
    def create(cls , time = None):
        if time is None:
            time = timezone.now()
        return time.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def now(cls):
        return timezone.now()



class SensorType( Model ):
    product_name = CharField( "Product name" , max_length = 256 )
    short_description = CharField("Short description" , max_length = 40)
    measurement_type = ForeignKey( MeasurementType )
    description = CharField("Description" , max_length = 256 )
    unit = CharField("Unit" , max_length = 60 )
    min_value = FloatField("Minimum value")
    max_value = FloatField("Maximum value")

    def __unicode__(self):
        return self.short_description


    def valid_range(self , value):
        if self.min_value <= value <= self.max_value:
            return True
        else:
            return False


    def valid_input(self , value):
        if not isinstance(value,float):
            try:
                value = float(value)
            except:
                return False
            
        return self.valid_range( value )



class Sensor( Model ):
    IDPattern = "[-_:a-zA-Z0-9]+"

    id = CharField("Sensor ID" , max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    sensor_type = ForeignKey( SensorType )
    parent_device = ForeignKey( Device )
    data_type = ForeignKey( DataType , default = "TEST" )
    description = CharField("Description" , max_length = 256 )
    on_line = BooleanField( default = True )
    last_value = FloatField( null = True , blank = True)
    last_timestamp = DateTimeField( null = True , blank = True) 

    def __unicode__(self):
        return self.id
        

    def valid_input(self , input_value):
        return self.sensor_type.valid_input( input_value )



    # Can speicify *either* a start or number of values with keyword
    # arguments 'start' and 'num', but not both. Will search in the
    # RawData table, only VALID data is considered.
    def get_ts(self, num = None , start = None):
        return RawData.get_ts( self , num = num, start = start)


    def get_vectors(self , num = None , start = None):
        return RawData.get_vectors( self , num = num , start = start)
        

    def get_current(self , timeout_seconds):
        current = {}
        data_value = DataValue.objects.select_related('data_info__timestamp').filter( data_info__sensor = self).order_by('data_info__timestamp__timestamp').last()
        if data_value is None:
            return None
            
        ts = data_value.data_info.timestamp.timestamp
        value = data_value.value
        if timeout_seconds > 0:
            if timezone.now() - ts > datetime.timedelta( seconds = timeout_seconds ):
                value = None
                

        location = data_value.data_info.location
        return {"sensorid"  : self.id,
                "timestamp" : data_value.data_info.timestamp.timestamp,
                "value"     : value,
                "location"  : {"latitude" : location.latitude , "longitude" : location.longitude}}


    def valid_post_key( self , key_string):
        return self.parent_device.valid_post_key( key_string )


    # This method returns a QuerySet - because that query set is
    # subsequently used to update the status of all the relevant
    # RawData records.
    def get_rawdata(self, status = RawData.VALID):
        qs = RawData.objects.filter( sensor_id = self.id , 
                                     processed = False ,
                                     status = status ).values_list( 'id', 'timestamp_data' , 'value').order_by('timestamp_data')
        
        return qs



