import json
import requests
import time
import datetime 

from django.conf import settings

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import sensor.models as models
from sensor.api.serializers import *
from sensor.api.info_serializers import *

        

class MeasurementTypeListView(generics.ListCreateAPIView):
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    


class MeasurementTypeView(generics.RetrieveAPIView):    
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    

#################################################################


class DeviceTypeListView(generics.ListCreateAPIView):
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    

class DeviceTypeView(generics.RetrieveAPIView):    
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

#################################################################

class DeviceListView(generics.ListCreateAPIView):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer
    

class DeviceView(generics.RetrieveAPIView):    
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer

#################################################################

class LocationListView(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    

class LocationView(generics.RetrieveAPIView):    
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

#################################################################


class DataTypeListView(generics.ListCreateAPIView):
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer
    

class DataTypeView(generics.RetrieveAPIView):    
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer


#################################################################

class DataInfoListView(generics.ListCreateAPIView):
    queryset = models.DataInfo.objects.all()
    serializer_class = DataInfoSerializer
    

class DataInfoView(generics.RetrieveAPIView):    
    queryset = models.DataInfo.objects.all()
    serializer_class = DataInfoSerializer

#################################################################

class DataValueListView(generics.ListCreateAPIView):
    queryset = models.DataValue.objects.all()
    serializer_class = DataValueSerializer
    

class DataValueView(generics.RetrieveAPIView):    
    queryset = models.DataValue.objects.all()
    serializer_class = DataValueSerializer

#################################################################


class TimeStampListView(generics.ListCreateAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer
    

class TimeStampView(generics.RetrieveAPIView):    
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


#################################################################


class SensorListView(generics.ListCreateAPIView):
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer
    

class SensorView(generics.RetrieveAPIView):    
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer


#################################################################

class SensorTypeListView(generics.ListCreateAPIView):
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer
    

class SensorTypeView(generics.RetrieveAPIView):    
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer


#################################################################


class SensorInfoView(APIView):
    def get(self , request , sensor_id = None):
        if sensor_id is None:
            sensor_list = models.Sensor.objects.all()
        else:
            try:
                sensor_list = [ models.Sensor.objects.get( pk = sensor_id ) ]
            except models.Sensor.DoesNotExist:
                return Response("The sensorID:%s is not found" % sensor_id , status.HTTP_404_NOT_FOUND)
            
        result = []
        for sensor in sensor_list:
            serialized = SensorInfoSerializer( sensor )
            data = serialized.data
            #current = sensor.get_current( CurrentValueView.DEFAULT_TIMEOUT )
            current = None
            if current is None:
                data["current_value"] = None
                data["current_timestamp"] = None
            else:
                data["current_value"] = current["value"]
                data["current_timestamp"] = current["timestamp"]

            result.append( data )
            
        if sensor_id is None:
            return Response( result , status = status.HTTP_200_OK ) 
        else:
            return Response( result[0] , status = status.HTTP_200_OK ) 


class ReadingView(APIView):

    def cleanPayload(self , data):
        if "sensorid" in data:
            sensorid = data["sensorid"]
        else:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'sensorid' field in payload")

                    
        if "value" in data:
            value = data["value"]
        else:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'value' field in payload")

        if not "timestamp" in data:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'timestamp' field in payload")

        try:
            sensor = models.Sensor.objects.get( pk = sensorid )
            if not sensor.valid_input( value ):
                return (status.HTTP_400_BAD_REQUEST , "The value:%s for sensor:%s is invalid" % (value , sensorid))

            if sensor.location is None:
                if not "location" in data:
                    return (status.HTTP_400_BAD_REQUEST , "Sensor:%s does not have location - must supply in post" % sensorid)
                        
        except models.Sensor.DoesNotExist:
            return (status.HTTP_404_NOT_FOUND , "The sensorID:%s is not found" % sensorid)
            
        return (True , "")


    def restdb_io_post( self , data ):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_POST_KEY}

        post_data = json.dumps( data )
        response = requests.post( settings.RESTDB_IO_URL , data = post_data , headers = headers )
        if response.status_code != status.HTTP_201_CREATED:
            return (response.status_code , response.text)

        return (status.HTTP_201_CREATED , 1)


    def post(self , request , format = None):
        try:
            raw_data = RawData.create( request.data )
        except ValueError:
            return Response(RawData.error( request.data ) , status = status.HTTP_400_BAD_REQUEST )
        

        key = raw_data.apikey
        sensorid = raw_data.sensor_id
        value = raw_data.value
        timestamp = raw_data.timestamp_data
        location = None
        try:
            sensor = models.Sensor.objects.get( pk = sensorid )
        except models.Sensor.DoesNotExist:
            return Response("The sensorID:%s is not found. " % sensorid , status.HTTP_404_NOT_FOUND)

        if not sensor.valid_post_key( key ):
            return Response("Invalid key:'%s' when posting to:'%s'" % (key , sensorid) , status.HTTP_403_FORBIDDEN)
            
        if not sensor.valid_input( value ):
            return Response("The value:%s for sensor:%s is invalid" % (value , sensorid) , status.HTTP_400_BAD_REQUEST)
        value = float(value)

        if sensor.location is None:
            if not "location" in request.data:
                return Response("Sensor:%s does not have location - must supply in post" % sensorid , status.HTTP_400_BAD_REQUEST)
            location = request.data["location"]
                    

        if sensor.on_line:
            ts = models.TimeStamp.objects.create( timestamp = timestamp )
            data_info = models.DataInfo( timestamp = ts , 
                                         sensor = sensor )
            if not location is None:
                data_info.location = location

            data_info.save()
            data_value = models.DataValue.objects.create( data_info = data_info ,
                                                          data_type = sensor.data_type ,  
                                                          value = value )
            sensor.last_value = value
            sensor.last_timestamp = timestamp
            sensor.save()

            raw_data.parsed = True
            raw_data.save( )

            if settings.RESTDB_IO_URL is None:
                return Response(1 , status.HTTP_201_CREATED)
            else:
                restdb_io_status , msg = self.restdb_io_post( {"key" : raw_data.apikey,
                                                               "sensorid" : raw_data.sensor_id,
                                                               "value" : value , 
                                                               "timestamp" : raw_data.timestamp_data.strftime("%Y-%m-%dT%H:%M:%S") } )

                if restdb_io_status == status.HTTP_201_CREATED:
                    return Response(msg , status = restdb_io_status)
                else:
                    return Response("Posting to restdb.io failed: %s" % msg , status = status.HTTP_500_INTERNAL_SERVER_ERROR )
        else:
            return Response("Sensor: %s is offline - rawdata created and stored" % raw_data.sensor_id )
            



    def restdb_io_get(self , sensor_id , request_params):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_GET_KEY}
        query_string = json.dumps( {"sensorid" : sensor_id} )

        params = {"q" : query_string,
                  "sort" : "timestamp",
                  "dir" : 1 }
        params.update( request_params )
        if not "max" in params:
            params["max"] = 99999999

        response = requests.get( settings.RESTDB_IO_URL , headers = headers , params = params)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            time_series = []
            for reading in data:
                time_series.append( (reading["timestamp"] , reading["value"]) )
            return Response( time_series , status = response.status_code ) 
        else:
            return Response( response.data , status = response.status_code ) 

        

    def get(self , request , sensor_id = None):
        if sensor_id is None:
            return Response("Must supply sensorid when querying" , status = status.HTTP_400_BAD_REQUEST )
            
        try:
            if "num" in request.GET:
                num = int(request.GET["num"])
            else:
                num = None

            if "start" in request.GET:
                start = models.TimeStamp.parse_datetime( request.GET["start"] )
            else:
                start = None

            sensor = models.Sensor.objects.get( pk = sensor_id )
            ts = sensor.get_ts( num = num , start = start )
            return Response(ts , status = status.HTTP_200_OK )
            #return self.restdb_io_get( sensor_id , request.GET )
        except models.Sensor.DoesNotExist:
            return Response("No such sensor:%s" % sensor_id , status = status.HTTP_404_NOT_FOUND )
            
        



class CurrentValueView(APIView):
    # Data which is older than the timeout is not considered
    # 'current'; and None is returned for the value.
    DEFAULT_TIMEOUT = 3600


    def get(self , request , sensor_id = None):
        if "mtype" in request.GET:
            mtype_id = int(request.GET["mtype"])
            try:
                mtype = models.MeasurementType.objects.get( pk = mtype_id )
            except models.MeasurementType.DoesNotExist:
                return Response("No such measuremenent type id:%s" % mtype_id , status = status.HTTP_404_NOT_FOUND )
        else:
            mtype = None

        timeout = CurrentValueView.DEFAULT_TIMEOUT
        if "timeout" in request.GET:
            timeout = int( request.GET["timeout"])

        if not sensor_id is None:
            try:
                sensor = models.Sensor.objects.get( pk = sensor_id )
            except models.Sensor.DoesNotExist:
                return Response("No such sensor:%s" % sensor_id , status = status.HTTP_404_NOT_FOUND )

            if not mtype is None:
                if sensor.sensor_type.measurement_type != mtype:
                    return Response("Measurement type mismatch" , status = status.HTTP_400_BAD_REQUEST )

            data = sensor.get_current( timeout )
            if data is None:
                return Response("No current data" , status = status.HTTP_404_NOT_FOUND)
            else:
                return Response( data )
        else:
            if mtype is None:
                sensor_list = models.Sensor.objects.all( )
            else:
                sensor_list = models.Sensor.objects.filter( sensor_type__measurement_type = mtype )
            
            data = []
            for sensor in sensor_list:
                sensor_data = sensor.get_current( timeout ) 
                if sensor_data is None:
                    sensor_data = {"sensorid" : sensor.id }
                data.append( sensor_data )
                
            return Response( data )


class RawDataView(APIView):

    def get(self , request , sensor_id = None):
        try:
            sensor = models.Sensor.objects.get( pk = sensor_id )
        except models.Sensor.DoesNotExist:
            return Response("The sensorID:%s is not found" % sensor_id , status = 404)#status.HTTP_404_NOT_FOUND)

        if "status" in request.GET:
            try:
                data_status = int( request.GET["status"] )
            except ValueError:
                return Response("The status: %s is invalid" % request.GET["status"] , status = 400)#status.HTTP_400_BAD_REQUEST )

            if not models.RawData.valid_status( data_status ):
                return Response("The status: %s is invalid" % request.GET["status"] , status = 400)#status.HTTP_400_BAD_REQUEST )
        else:
            data_status = models.RawData.RAWDATA
        
        query = models.RawData.objects.filter( sensor_id = sensor.id , 
                                               status = data_status )
        data = []
        for row in query:
            data.append( (row.timestamp_data , row.string_value ))
        
        return Response( data )
                                       
