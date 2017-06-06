from django.db.models import *

# This app/model is no longer in use, but we must retain it
# in the project to ensure that the migrations play nicely.

class GitVersion(Model):
    ref = CharField("Git ref" , max_length = 128 )
    repo = CharField("Git repo" , max_length = 128 , default = "https://github.com/FriskbyBergen/RPiParticle")
    follow_head = BooleanField( default = False )
    description = CharField("Description" , max_length = 256 )


