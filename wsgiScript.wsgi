
import sys
import os

from handleDbStart import initDb
from bot import initBot
from wsgi import wsgi as application
initDb()
initDiscord()