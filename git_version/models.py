from __future__ import unicode_literals
import requests

from django.core.exceptions import ValidationError
from django.db.models import *

class GitVersion(Model):
    ref = CharField("Git ref" , max_length = 128 )
    repo = CharField("Git repo" , max_length = 128 , default = "https://github.com/FriskbyBergen/RPiParticle")
    follow_head = BooleanField( default = False )
    description = CharField("Description" , max_length = 256 )


    def __unicode__(self):
        return "%s: %s" % (self.description , self.ref)


    def save(self, *args, **kwargs):
        if "github.com" in self.repo:
            self.validateGithubRepo( )
        
        super(GitVersion , self).save( *args , **kwargs )
        


    def validateGithubRepo( self ):
        com_find = self.repo.find( "com" )
        owner_repo = self.repo[com_find + 4:]
        url = "https://api.github.com/repos/%s/commits/%s" % (owner_repo , self.ref)
        # refs: https://developer.github.com/v3/git/refs/heads/branch
        response = requests.get( url )
        if response.status_code != 200:
            raise ValidationError("Could not fetch ref:%s from:%s " % (self.ref , self.repo))
