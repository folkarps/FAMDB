FAMDB
=====

ArmAx missions database written in python3 and jQuery

FAMDB is designed to simplify the lives of admins and hosts.

Users can create and edit mission descriptions, upload mission versions, and
schedule deletion of specific versions of missions.

Admins can move missions from the mission making server (MM server) to the main server, archive missions,
and create sessions with specific missions.

Issues can be reported at https://github.com/Raptoer/FAMDB/issues

Usage
=====
After python 3.5+, pip and git have been installed run

sudo pip install -e git+git://github.com/Raptoer/FAMDB.git@master#egg=FAMDB

This will download FAMDB to the current directory.
Then run 

pip install -r requirementsPosix.txt or pip install -r requirementsWindows.txt depending on your environment

windows users will then have to install pycrypt manually using a command that I lost.

FAMDB runs as a WSGI server. This means it can be run using either apache's mod_wsgi (as we do) or a wsgi server built into python.

Starting the server:
python main.py start

Stopping the server:
python main.py stop

server can be started manually using 
python startServer.py
However this starts a foreground process

Configuration
=============
in the file config.config there are a number of properties:
* 4 folders, 2 for the missions and 2 for archives
* Port on which the built in server should run. This is ignored if using an external wsgi server.
* email address for the recover password feature
* email password for the recover password feature
* email Server for the recover password feature
* email sever for the recover password feature
* external server address for the recover password feature
 
Please ensure that the user running the server has permissions to access these folders, as well as the entire famdb folder structure.

Database
========
FAMDB uses sqlite and as such stores its data in a file named famdb.db
If you need to wipe your data, just delete this file.
It is suggested that you back up this file occasionally

Credits
=====
* Fer
* Head
* Tigershark
* Wolfenswan
* Pooter
