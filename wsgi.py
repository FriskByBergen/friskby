import os
import sys

sys.path.append( os.path.dirname( __file__ ))

os.environ['DJANGO_SETTINGS_MODULE'] = 'friskby.settings'

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
