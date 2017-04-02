import datetime
import pytz

from django.core.urlresolvers import reverse
from django.utils import dateparse, timezone
from django.db.models import (Model, BooleanField, CharField, DateTimeField,
                              FloatField, ForeignKey, IntegerField, TextField)
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from api_key.models import ApiKey
from git_version.models import GitVersion



class MeasurementType(Model):
    name = CharField("Type of measurement", max_length=60, unique = True)

    def __unicode__(self):
        return self.name



class Location(Model):
    name = CharField("Location", max_length=60)
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    altitude = FloatField("Altitude", null=True)

    def __unicode__(self):
        return self.name



class DeviceType(Model):
    name = CharField("Name of the device", max_length=60)

    def __unicode__(self):
        return self.name



class Device(Model):
    IDPattern = "[-_:a-zA-Z0-9]+"

    id = CharField("Device ID",
                   max_length=60,
                   primary_key=True,
                   validators=[RegexValidator(regex="^%s$" % IDPattern)])
    location = ForeignKey(Location, null=True)
    device_type = ForeignKey(DeviceType)
    description = CharField("Description", max_length=256)
    post_key = ForeignKey(ApiKey)
    client_version = CharField(max_length=128, blank=True, null=True)
    git_version = ForeignKey(GitVersion, blank=True, null=True)
    locked = BooleanField(default=True)
    owner = ForeignKey(User)


    def __unicode__(self):
        return self.id

    def valid_post_key(self, key_string):
        return self.post_key.access(key_string)

    def sensorList(self):
        return Sensor.objects.filter(parent_device=self)

    def clientConfig(self):
        # The post key is not set here, and must be explicitly set in the
        # view code if the request is correctly authorized.
        config = {"sensor_list" : [sensor.sensor_id for sensor in self.sensorList()],
                  "post_path" : reverse("sensor.api.post"),
                  "config_path" : reverse("sensor.device_config", args=[self.id]),
                  "device_id" : self.id}

        if self.git_version:
            config["git_repo"] = self.git_version.repo
            config["git_ref"] = self.git_version.ref
            config["git_follow"] = self.git_version.follow_head
        return config

    def lockDevice(self):
        if self.locked == False:
            self.locked = True
            self.save()



class SensorType(Model):
    product_name = CharField("Product name", max_length=256)
    short_description = CharField("Short description", max_length=40)
    measurement_type = ForeignKey(MeasurementType)
    description = CharField("Description", max_length=256)
    unit = CharField("Unit", max_length=60)
    min_value = FloatField("Minimum value")
    max_value = FloatField("Maximum value")

    def __unicode__(self):
        return self.short_description

    def valid_range(self, value):
        return self.min_value <= value <= self.max_value

    def valid_input(self, value):
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                return False
        return self.valid_range(value)



class DataType(Model):
    id = CharField("DataType", max_length=60, primary_key=True)

    def __unicode__(self):
        return self.id



class Sensor(Model):
    IDPattern = "[-_:a-zA-Z0-9]+"

    s_id = IntegerField(primary_key=True)
    sensor_id = CharField("Sensor ID",
                          unique = True, 
                          max_length=60,
                          validators=[RegexValidator(regex="^%s$" % IDPattern)])
    sensor_type = ForeignKey(SensorType)
    parent_device = ForeignKey(Device)
    data_type = ForeignKey(DataType, default="TEST")
    description = CharField("Description", max_length=256)
    on_line = BooleanField(default=True)
    last_value = FloatField(null=True, blank=True)
    last_timestamp = DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.sensor_id

    def valid_input(self, input_value):
        return self.sensor_type.valid_input(input_value)


    # Can speicify *either* a start or number of values with keyword
    # arguments 'start' and 'num', but not both.
    def get_ts(self, num=None, start=None, end=None):
        return RawData.get_ts(self, num=num, start=start, end=end)


    def get_vectors(self, num=None, start=None, end=None):
        return RawData.get_vectors(self, num=num, start=start, end=end)


    def get_current(self, timeout_seconds):
        current = {}
        data_value = DataValue.objects.select_related('data_info__timestamp').filter(data_info__sensor=self).order_by('data_info__timestamp__timestamp').last()
        if data_value is None:
            return None

        ts = data_value.data_info.timestamp.timestamp
        value = data_value.value
        if timeout_seconds > 0 and timezone.now() - ts > datetime.timedelta(seconds=timeout_seconds):
            value = None

        location = data_value.data_info.location
        return {"sensorid"  : self.sensor_id,
                "timestamp" : data_value.data_info.timestamp.timestamp,
                "value"     : value,
                "location"  : {"latitude" : location.latitude, "longitude" : location.longitude}}


    def valid_post_key(self, key_string):
        return self.parent_device.valid_post_key(key_string)


    # This method returns a QuerySet - because that query set is
    # subsequently used to update the status of all the relevant
    # RawData records.
    def get_rawdata(self):
        qs = RawData.objects.filter(sensor_string_id=self.sensor_id,
                                    processed=False).values_list('id',
                                                                 'timestamp_data',
                                                                 'value').order_by('timestamp_data')

        return qs



class RawData(Model):
    sensor_string_id = CharField(max_length=128)
    s_id = ForeignKey(Sensor)
    timestamp_recieved = DateTimeField()
    timestamp_data = DateTimeField()
    value = FloatField(default=-1)
    processed = BooleanField(default=False)

    def __unicode__(self):
        return "Sensor:%s: Value:%s" % (self.sensor_string_id, self.value)


    def save(self, *args, **kwargs):
        if self.timestamp_recieved is None:
            self.timestamp_recieved = datetime.datetime.now(pytz.utc)
        super(RawData, self).save(*args, **kwargs)

    @classmethod
    def error(cls, data):
        if data is None:
            return "Error: empty payload"

        missing_keys = []
        for key in ["key", "value", "timestamp"]:
            if not key in data:
                missing_keys.append(key)

        if "sensor_id" not in data and "id" not in data:
            missing_keys.append("id")

        if missing_keys:
            return "Error: missing fields in payload: %s" % missing_keys

        ts = TimeStamp.parse_datetime(data["timestamp"])
        if ts is None:
            return "Error: invalid timestamp - expected: %s" % TimeStamp.DATETIME_FORMAT

        return None

    @classmethod
    def get_ts(cls, sensor, num=None, start=None, end=None):
        ts = []
        if num is None:
            if start is None and end is None:
                qs = RawData.objects.filter(sensor_string_id=sensor.sensor_id).order_by('timestamp_data')
            else:
                if end is None:
                    qs = RawData.objects.filter(sensor_string_id=sensor.sensor_id,
                                                timestamp_data__gte=start).order_by('timestamp_data')
                elif start is None:
                    qs = RawData.objects.filter(sensor_string_id=sensor.sensor_id,
                                                timestamp_data__lte=end).order_by('timestamp_data')
                else:
                    qs = RawData.objects.filter(sensor_string_id=sensor.sensor_id,
                                                timestamp_data__range=[start, end]).order_by('timestamp_data')

        else:
            if start is None and end is None:
                qs = reversed(RawData.objects.filter(sensor_string_id=sensor.sensor_id).order_by('-timestamp_data')[:num])
            else:
                raise ValueError("Can not supply both num and start")

        for entry in qs:
            ts.append((entry.timestamp_data, entry.value))
        return ts


    @classmethod
    def get_vectors(cls, sensor, num=None, start=None, end=None):
        pairs = cls.get_ts(sensor, num=num, start=start, end=end)
        ts = []
        values = []
        for (t, v) in pairs:
            ts.append(t)
            values.append(v)

        return ts, values


    @classmethod
    def create(cls, data):
        if "id" in data:
            (dev_id,mt) = data["id"]

            try:
                device = Device.objects.get( pk = dev_id )
            except Device.DoesNotExist:
                raise ValueError("No such device: %s" % dev_id)

            try:
                mtype = MeasurementType.objects.get( name = mt )
            except MeasurementType.DoesNotExist:
                raise ValueError("No such measurement type: %s" % mt)


            # The data model is somewhat broken here; the assumption
            # is that a devide_id and a measurement type should
            # uniquely define a sensor, but that is actually not
            # reflected in the data model.
            #
            # That is reflected in the except: clauses below which
            # catch both the DoesNotExist and the
            # MultipleObjectsReturned exceptions.
            try:
                stype = SensorType.objects.get( measurement_type = mtype )
            except (SensorType.DoesNotExist, SensorType.MultipleObjectsReturned):
                raise ValueError("Internal error: not exactly one sensortype corresponding to measurment type:%s" % mtype)

            try:
                sensor = Sensor.objects.get( parent_device = device, sensor_type = stype )
            except (Sensor.DoesNotExist, Sensor.MultipleObjectsReturned):
                raise ValueError("Internal error: not exactly one sensor corresponding to (%s,%s)" % (device, mtype))
            sensor_string_id = sensor.sensor_id

        elif "sensorid" in data:
            sensor_string_id = data["sensorid"]
            try:
                sensor = Sensor.objects.get(sensor_id=sensor_string_id)
            except Sensor.DoesNotExist:
                raise ValueError("No such sensor: %s" % sensor_string_id)
        else:
            raise ValueError("Must have 'sensorid' or 'id' as part of data")

        if "key" in data:
            key = data["key"]
            if not sensor.valid_post_key(key):
                raise ValueError("Invalid post key:'%s' for sensor:'%s'" % (key, sensor_string_id))
        else:
            raise ValueError("Must have 'key' in data")

        if not sensor.on_line:
            raise ValueError("Sensor '%s' is offline - can not accept data")

        string_values = []
        string_ts = []
        if "value" in data and "timestamp" in data:
            string_values.append(data["value"])
            string_ts.append(data["timestamp"])
        elif "value_list" in data:
            for ts, value in data["value_list"]:
                string_ts.append(ts)
                string_values.append(value)
        else:
            raise ValueError("Missing 'data' and 'timestamp' or 'value_list'")

        timestamp = []
        values = []
        try:
            for ts, string_value in zip(string_ts, string_values):
                timestamp.append(TimeStamp.parse_datetime(ts))
                value = float(string_value)
                if not sensor.sensor_type.valid_range(value):
                    raise ValueError("Out of range")
                values.append(value)
        except:
            raise ValueError("Invalid data")

        rawdata = []
        for ts, value in zip(timestamp, values):
            rd = RawData(sensor_string_id=sensor.sensor_id,
                         s_id=sensor,
                         timestamp_data=ts,
                         value=value)
            rd.save()
            rawdata.append(rd)
        return rawdata



class TimeStamp(Model):
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    # When parsing a string the format should be as: "2015-10-10T10:10:00+01";
    # i.e. yyyy-mm-ddTHH:MM:SS+zz
    # Where the +zz is a timezone shift relative to UTC; i.e. +01 for Central European Time.

    @classmethod
    # This takes a time_string which is supposed to be in the time
    # zone given by the settings.TIME_ZONE variable. The resulting
    # dt variable is a time zone aware datetime instance.
    def parse_datetime(cls, time_string):
        dt = dateparse.parse_datetime(time_string)
        return dt

    @classmethod
    def create(cls, time=None, format=None, locale=False):
        if format is None:
            format = cls.DATETIME_FORMAT
        if time is None:
            time = timezone.now()
        if locale:
            time = timezone.localtime(time)
        return time.strftime(format)

    @classmethod
    def now(cls):
        return timezone.now()
    
    @classmethod
    def timezoneOffset(cls):
        return -1*timezone.localtime(timezone.now()).utcoffset().seconds/60


class ClientLog(Model):
    device = ForeignKey(Device)
    timestamp = DateTimeField()
    msg = CharField(max_length=256)
    long_msg = TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.timestamp = datetime.datetime.now(pytz.utc)
        super(ClientLog, self).save(*args, **kwargs)

    def __unicode__(self):
        return "[%s] %s: %s" % (self.device, self.timestamp, self.msg)
