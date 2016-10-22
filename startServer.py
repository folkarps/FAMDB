import os
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

import utils
import wsgi
from handleDbStart import initDb

initDb()

print('starting server...')

# Server settings

path = Path("famdb.pid")
if path.exists():
    file = open("famdb.pid", "r")
    pid = int(list(file)[0])
    serverRunning = utils.isPidRunning(pid)
    if serverRunning:
        print('Fatal:Detecting server already running as pid:' + str(pid) + "\nPlease kill this first",
              file=sys.stderr)
        exit()
    else:
        print('Warning:PID file detected, but no running process found, continuing')
file = open("famdb.pid", "w+")
file.write(str(os.getpid()))
file.close()

print('running server...')
httpd = make_server('', utils.port, wsgi.wsgi)
httpd.serve_forever()
