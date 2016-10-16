FAMDB
=====

ArmAx missions database written in python3 and jQuery

FAMDB is designed to simplify the lives of admins and hosts.

Users can create and edit mission descriptions, upload mission versions, and
schedule deletion or archival of specific versions of missions.

Admins can move missions from the mission making server (MM server) to the main server
and create sessions with specific missions.

Issues can be reported at https://github.com/Raptoer/FAMDB/issues

Usage
=====

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
* Port on which the server should run
 
Please ensure that the user running the server has permissions to access these folders

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