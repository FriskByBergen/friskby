import requests
import datetime
import json

ROOT_URL = "https://friskby.herokuapp.com/"


class FriskByHttp(object):
    def __init__(self , url):
        self.url = url


    def getRootURL(self):
        return self.url

    
    def getFromURL(self , api_url , params = None):
        url = self.url + api_url
        response = requests.get( url , params = params)
        if response.status_code == 200:
            return response.json( )
        else:
            raise Exception("Query to:%s returned status code:%s Error:%s" % (url , response.status_code , response.text))


    def postToURL(self , api_url , data , params = None ):
        url = self.url + api_url
        response = requests.post(url , data = json.dumps( data ) , headers = {"Content-Type" : "application/json"})
        if response.status_code != 201:
            raise Exception("Post failed: %s" % response.text)
            


            
class FriskBySensor(FriskByHttp):
    def __init__(self , values , url = ROOT_URL , key = None):
        super(FriskBySensor , self).__init__( url )
        sensor_type = values["sensor_type"]
        self.id = values["id"]
        self.min_value = sensor_type["min_value"]
        self.max_value = sensor_type["max_value"]
        self.post_key = key


    @classmethod
    # If this does not have an explicit timezone, it will be
    # interpreted according to the TIME_ZONE variable in settings.
    def timeStamp(cls , time = None):
        if time is None:
            time = datetime.datetime.now()
            
        return time.strftime("%Y-%m-%dT%H:%M:%S")


    def getMinValue(self):
        return self.min_value


    def getMaxValue(self):
        return self.max_value


    def getLastValue(self):
        data = self.getFromURL( "sensor/api/reading/%s/" % self.id , params = {"sort" : "_id" , "dir" : -1 , "max" : 1})
        if len(data) == 1:
            return data[0]
        else:
            raise Exception("No data for sensor:%s" % self.id)
            
    def getData(self):
        data = self.getFromURL( "sensor/api/reading/%s/" % self.id , params = {"sort" : "_id"})
        if len(data) > 0:
            return data
        else:
            raise Exception("No data for sensor:%s" % self.id)
        


    def postValue(self , value , timestamp = None):
        if timestamp is None:
            timestamp = self.timeStamp( )

        data = {"value" : value , "timestamp" : timestamp , "sensorid" : self.id }
        if not self.post_key is None:
            data["key"] = self.post_key
        self.postToURL( "sensor/api/reading/" , data )


class FriskByGW(FriskByHttp):

    def __init__(self , url = ROOT_URL):
        super(FriskByGW , self).__init__( url )

    
    def sensorList(self):
        sensor_list = []
        sensor_data = self.getFromURL( "sensor/api/sensorinfo/")
        for data in sensor_data:
            sensor_list.append( FriskBySensor( data , self.url ))
        return sensor_list

    
    def getSensor(self , sensorid , key = None ):
        try:
            sensor_data = self.getFromURL( "sensor/api/sensorinfo/%s/" % sensorid)
            return FriskBySensor( sensor_data , self.url , key )
        except Exception:
            sensor = None
        return sensor
