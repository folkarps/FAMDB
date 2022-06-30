FAMDB
=====

ArmAx missions database written in python3 and jQuery

FAMDB is designed to simplify the lives of admins and hosts.

FolkArps's instance of FAMDB can be seen at https://famdb.folkarps.com/

Users can create and edit mission descriptions, upload mission versions, and
schedule deletion of specific versions of missions.

Admins can move missions from the mission making server (MM server) to the main server, 
and create sessions with specific missions.

Issues can be reported at https://github.com/folkarps/FAMDB/issues

Usage
=====
After python 3.9+, pip and git have been installed run

git clone https://github.com/folkarps/FAMDB.git -b master

This will download FAMDB to the current directory.
Then run 

pip3 install .

FAMDB runs as a WSGI server. 

You have 2 options to run FAMDB
1. Running using apache or nginx WSGI server. This is recommended.
  
     For apache there are two directives that are necessary.
  
      1. WSGIPythonPath
        This tells python where to look for the files
      2. WSGIScriptAlias
          This tells apache when and how to route requests to FAMDB. point it to the wsgiScript.wsgi file


2. Running using python's built in WSGI server.

     Starting the server:
     python main.py start

     Stopping the server:
     python main.py stop

Configuration
=============
in the file config.config there are a number of properties:
* 2 folders for mission pbos (one for testing server, and one for main server)
* Port on which the built in server should run. This is ignored if using an external wsgi server.
* email address for the recover password feature
* email password for the recover password feature
* email Server for the recover password feature
* email sever for the recover password feature
* external server address for the recover password feature
* discord admin role ID
* discord webhook url
 
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
* Lexer

For help contact Lexer on discord at on the FolkArps discord (Link found at https://www.folkarps.com)
