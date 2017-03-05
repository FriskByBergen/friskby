from django.urls import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from .context import TestContext
from sensor.models import *
from friskby.views.quick import downsample
from datetime import datetime as dt

class QuickTest(TestCase):
    def setUp(self):
        self.context = TestContext( )

    def test_downsample_time(self):
        def gen_date(minut):
            return dt(2017,1,1,1,minut,1)
        data = []
        num_points = 53
        for i in range(num_points):
            data.append({'value': i, 'timestamp_data': gen_date(i)})
        dsda = downsample(data, minutes=7, cutoff=41.0)
        self.assertEqual(8, len(dsda))
        self.assertEqual(gen_date(num_points-1), dsda[-1]['timestamp_data'])
        self.assertEqual(41.0, dsda[-1]['value'])


    def test_downsample_maxval(self):
        self.assertEqual([], downsample([]))
        maxval = 123.45
        e = {'value': 150, 'timestamp_data': dt.now()}
        x = downsample([e], cutoff=maxval)
        e_ds = x[0]
        self.assertEqual(1, len(x))
        self.assertEqual(maxval, e_ds['value'])

    def test_get(self):
        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url)
        self.assertEqual( response.status_code , status.HTTP_200_OK )


    def test_time_param(self):
        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url , {"time" : "2016-10-10T12:12:00+01" } )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

    def test_invalid_mtypes(self):
        mtype10 = MeasurementType.objects.get( name = "PM10" )
        mtype10.name = "PM10_modified"
        mtype10.save( )

        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url)

        self.assertEqual( response.status_code , status.HTTP_500_INTERNAL_SERVER_ERROR )
