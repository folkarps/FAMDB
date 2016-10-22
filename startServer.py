import sys
from wsgiref.simple_server import make_server

import utils
import wsgi

print(sys.path)

httpd = make_server('', utils.port, wsgi.wsgi)
httpd.serve_forever()
