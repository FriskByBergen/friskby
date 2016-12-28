from django.urls import reverse
from django.test import TestCase, Client
from rest_framework import status


class PlotRootTest(TestCase):
    def setUp(self):
        pass

    def test_get_list(self):
        client = Client( )
        response = client.get( reverse("plot_root.view") )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
