import requests
import datetime
import json

ROOT_URL = "https://friskby.herokuapp.com/"


class FriskByHttp(object):
    def __init__(self , url = ROOT_URL):
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


            
class FriskBySensor(FriskByHttp):
    def __init__(self , values , url = ROOT_URL):
        super(FriskBySensor , self).__init__( ROOT_URL )
        self.id = values["id"]
        self.min_value = values["min_value"]
        self.max_value = values["max_value"]


    def timeStamp(self, time = None):
        if time is None:
            time = datetime.datetime.now()
            
        return time.strftime("%Y-%m-%d %H:%M:%S")


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
            

    def postValue(self , value):
        url = self.url + "sensor/api/reading/"
        timestamp = self.timeStamp( )
        data = []
        try:
            for v in value:
                data.append( {"value" : v , "timestamp" : timestamp , "sensorid" : self.id } ) 
        except TypeError:
            data.append( {"value" : value , "timestamp" : timestamp , "sensorid" : self.id } ) 
            
        response = requests.post(url , data = json.dumps( data ) , headers = {"content_type" :  "application/json"})
        if response.status_code != 201:
            raise Exception("Post failed: %s" % response.text)



class FriskByGW(FriskByHttp):

    def __init__(self , url = ROOT_URL):
        super(FriskByGW , self).__init__( ROOT_URL )

    
    def sensorList(self):
        sensor_list = []
        sensor_data = self.getFromURL( "sensor/api/sensorID/")
        for data in sensor_data:
            sensor_list.append( FriskBySensor( data , self.url ))
        return sensor_list

    
    def getSensor(self , sensorid):
        try:
            sensor_data = self.getFromURL( "sensor/api/sensorID/%s/" % sensorid)
            return FriskBySensor( sensor_data , self.url )
        except Exception:
            sensor = None
        return sensor
