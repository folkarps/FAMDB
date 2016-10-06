import json
import sqlite3


def handleAuthors(request):
    conn = sqlite3.connect('famdb.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select distinct missionAuthor from missions order by missionAuthor")
    authors = c.fetchall()
    authorDto = [x['missionAuthor'] for x in authors]
    encode = json.dumps(authorDto).encode()
    request.wfile.write(encode)
    return
