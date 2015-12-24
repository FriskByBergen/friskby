from django.db.models.signals import post_init
from django.dispatch import receiver
from .models import *


@receiver( post_init , sender = TimeArray)
def model_post_init_TimeArray(sender , **kwargs):
    instance = kwargs["instance"]
    if instance.data is None:
        instance.data = TimeArray.createArray( )



@receiver( post_init , sender = SampledTimeSeries)
def model_post_init_ValueArray(sender , **kwargs):
    instance = kwargs["instance"]
    if instance.data is None:
        instance.data = SampledTimeSeries.createArray( )
    


@receiver( post_init , sender = RegularTimeSeries)
def model_post_init_RegularTimeSeries(sender , **kwargs):
    instance = kwargs["instance"]
    if instance.data is None:
        instance.data = RegularTimeSeries.createArray(  )
