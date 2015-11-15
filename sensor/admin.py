from django.contrib import admin
from models import *


@admin.register(DataValue)
class DataValueAdmin(admin.ModelAdmin):
    # Skip the data_info field - that creates a selector in the admin
    # which becomes prohibetively expensive to populate.
    fields = ('data_type','value')


admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(Company)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(MeasurementType)
admin.site.register(Location)
admin.site.register(DataType)
admin.site.register(RawData)
