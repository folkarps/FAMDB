from wsgiref.simple_server import make_server

import utils
import wsgi

httpd = make_server('', utils.port, wsgi.handleWSGI)
httpd.serve_forever()
