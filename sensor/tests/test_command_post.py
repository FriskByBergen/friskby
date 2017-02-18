from django.test import TestCase

from sensor.management.commands.post import Command as PostCommand
from .context import TestContext


class CommandPostTest(TestCase):
    
    def test_post(self):
        cmd = PostCommand( )
        
