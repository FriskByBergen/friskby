#!/usr/bin/env python
import sys
import os
import subprocess


def run_script( executable , arg_list ):
    if not os.path.isabs( executable ):
        executable = os.path.abspath( executable )

    subprocess.call( [executable] + arg_list )
    

def update_env(*args):
    for arg in args:
        var,value = arg.split("=")
        os.environ[var] = value
    
    if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
        os.environ["DJANGO_SETTINGS_MODULE"] = "friskby.settings"


    new_path = os.path.realpath( os.path.join( os.path.dirname(__file__) , "../../") )
    if os.environ.has_key("PYTHONPATH"):
        os.environ["PYTHONPATH"] = "%s:%s" % (new_path , os.environ["PYTHONPATH"])
    else:
        os.environ["PYTHONPATH"] = new_path
    



def assert_env():
    assert os.environ.has_key("DATABASE_URL")
    assert os.environ.has_key("DJANGO_SETTINGS_MODULE")

#-----------------------------------------------------------------

root = os.path.dirname( __file__)
os.chdir( root )

path_arg = sys.argv[1]
arg_list = sys.argv[2:]
update_env()
assert_env()

if os.path.isfile( path_arg ):
    run_script( path_arg , arg_list )
else: 
    for script in os.listdir( path_arg ):
        run_script( os.path.join(path_arg , script) , arg_list )


