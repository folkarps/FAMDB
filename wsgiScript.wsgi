
import sys
import os

from handleDbStart import initDb
from wsgi import wsgi as application
initDb()