from django.apps import AppConfig


class TimeSeriesConfig(AppConfig):
    name = 'time_series'
    verbose_name = 'Time series Application'
 
    def ready(self):
        import time_series.signals
