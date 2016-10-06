import sqlite3
from urllib.parse import urlparse, parse_qs


def handleSetUserLevel(request):
    conn = sqlite3.connect('famdb.db')
    c = conn.cursor()
    o = parse_qs(urlparse(request.path).query)
    userId = o['id']
    level = o['level']
    c.execute("update users set permissionLevel = ? where id = ?", [level, userId])
    return
