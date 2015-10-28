from django.contrib import admin
from models import *

admin.site.register(Sensor)
admin.site.register(Company)
admin.site.register(DeviceType)
admin.site.register(MeasurementType)
admin.site.register(Location)
admin.site.register(TimeStamp)
admin.site.register(DataType)
admin.site.register(DataInfo)
admin.site.register(DataValue)

