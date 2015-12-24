from django.contrib import admin

from models import *



@admin.register(TimeArray)
class TimearrayAdmin(admin.ModelAdmin):
    readonly_fields = ('id','start','end','length')


@admin.register(SampledTimeSeries)
class SampledTimeSeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('id','length','min','max','avg')


@admin.register(RegularTimeSeries)
class RegularTimeSeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('id','length','min','max','avg')
