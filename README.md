# FriskBy

This web service is part of the FriskBy project.

Air quality measurement devices can POST measurements to the
server. The server has a REST api which can be used to query the
stored data.

The web service is based on the Python web framework Django:
http://www.djangoproject.com. 


## Getting started

If you want to make modifications to the friskby web-server you must
go through some initial setup before you can start hacking. The
specific commandlines illustrated in this README assume that you are
using a Debian based Linux distribution, but there is nothing Debian
or even Linux specific to the software as such.


### Installing the dependencies (I)

You need to install the following packages: git, postgresql,
postgresql-server-dev-all and python-pip:

```bash
bash% sudo apt-get install git postgresql postgresql-server-dev-all python-pip
```

After pip has been installed, we install all the required Python packages by
giving the file `requirements.txt` to pip:

```bash
bash% sudo pip install -r requirements.txt
```

### Setting up the source code

Development of the source code is done on GitHub using a model with
personal forks. So to set up your environment for working with the friskby web service:

1. Create an account on GitHub.

2. Fork the friskby repository to your personal account. When you have
   done this you should have a personal repository:
   https://github.com/$USER/friskby.

3. Clone your repository down to your personal computer:

   ```bash
   bash% git clone git@github.com:$USER/friskby
   ```

4. Add the FriskByBergen/friskby repository as a remote repository:

   ```bash
   bash% git remote add upstream git@github.com:FriskByBergen/friskby
   ``` 

   This remote repository will be used when you should update your
   local git repository with the changes done by other developers.

The git/github workflows used by FriskBy are very common, and
extensive explanations are only a google search away.


### Creating the database

A database for storing the measurements is an essential part of the
friskby web service, and to develop on the source code for the web
server you need to have your own local database. Observe that Django
is quite database agnostic, and you could in principle use MySQL or
Sqlite instead of postgres for your own personal development. However
the friskby web server currently uses postgres in production, and
there is also a possibility that we would like to use postgres
extensions to Django in the future. The following guideline is
therefor based on postgres:

1. Change identity to `posgtgres`:

   ```bash
   bash% sudo su - postgres
   ```

2. Create a new user (role):

   ```bash
   bash% createuser friskby-user -P
   Enter password for new role: <friskby-pwd>
   Enter it again: <friskby-pwd>
   ```

   As indicated the `createuser` program will prompt for a password.

3. Create a new database - owned by the new user:

   ```bash
   bash% createdb friskby-db --owner=friskby-user
   ```

After these steps you should have made a database with name
`friskby-db` and user with credentials `(friskby-user,
friskby-pwd)`. These three values should be part of the `DATABASE_URL`
connection string - see the section about environment variables. Log
out of the `postgres` account and test the connection:

```bash
bash% psql friskby-db -U friskby-user -h localhost
```


### Environment variables

The configuration of the FriskBy web server is handled through the use
of environment variables. In Django configuration settings are read
from the `settings` namespace in the root of the project, in this
project the `settings/__init__.py` file contains several calls of the
type:

```python
SETTING_VARIABLE = os.getenv("SETTING_ENV_VARIABLE")
```

The file `init_env.sh.template` is a template file which includes the
environment variables you should set to run the FriskBy web
server. Follow the instructions in this file and create a personal
`init_env.sh` file, the `init_env.sh` file should *not* be under
version control.



### Testing the code

When you updated your environment you are ready to actually run the
friskby code. To run all the tests:

```python

    bash% ./manage.py test

```

To start the development server:

```python

   bash% ./manage.py runserver
```

Then you go to `http://127.0.0.1:8000` in your browser and interact
with your personal development copy of the FriskBy web server. 


### Developing and getting the code merged

When you are finished with your changes make a Pull Request on GitHub.


### Deploying the code

The FriskBy web server is deployed on Heroku. It should be quite
simple to deploy using an alternative platform.


### Creating testdata

To get some testdata to work with there are management commands. To
create three testsensors with random data:

```bash

   bash% manage.py add_testdevice TestDev1 TestDev2 TestDev3
```

This will by default add 100 random datapoints to each of the sensors,
but by passing `--num=nnn` you can add a different number of
points. The random devices can be removed with:

```bash

   bash% manage.py drop_testdevice TestDev1 TestDev3
```

which will remove the devices 'TestDev1' and 'TestDev3'. If you pass
the special argument '--all' to the 'drop_testdevice' managament
command *all* devices will be removed. 

In addition to the 'add_testdevice' and 'drop_testdevice' commands
there are commands 'add_testdata' and 'drop_testdata' which will only
add or drop testdata, not the actual devices.

```bash

   bash% manage.py add_testdata 
```

Will add 100 datapoints to each available sensor, by passing '--num='
you can control the number of points, and by passing '--device=' or
'--sensor=' you can control which sensor gets the data.


```bash

   bash% manage.py drop_testdata
```

will drop all the testdata. Pass '--device' or '--sensor'.
