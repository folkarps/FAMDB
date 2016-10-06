import sqlite3
from urllib.parse import urlparse, parse_qs


def handleArchive(request):
    conn = sqlite3.connect('famdb.db')
    c = conn.cursor()
    o = parse_qs(urlparse(request.path).query)
    c.executemany('''update versions set toBeArchived = 1 where origin = ? and name = ?''', {o['origin'], o['name']})
    return
