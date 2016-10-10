import gzip
import os
import shutil
from urllib.parse import urlparse, parse_qs

import utils


def handleCleanup(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)

    # if you're a low admin
    if not utils.checkUserPermissions(utils.getCurrentUser(request), 2):
        request.send_response(500)
        request.end_headers()
        request.wfile.write("Access Denied".encode())
        return

    if o['origin'] == 'main':
        missionDirPrefix = utils.missionMainDir
        missionArchivePrefix = utils.missionMainArchive
        toBeArchivedProperty = 'toBeArchivedMain'
        toBeDeletedProperty = 'toBeDeletedMain'
    else:
        missionDirPrefix = utils.missionMakerDir
        missionArchivePrefix = utils.missionMakerArchive
        toBeArchivedProperty = 'toBeArchivedMM'
        toBeDeletedProperty = 'toBeDeletedMM'

    c.execute('''select * from versions where ''' + toBeArchivedProperty + ''' = 1''', o['origin'])
    toBeArchived = c.fetchall()

    for forArchival in toBeArchived:
        with open(missionDirPrefix + forArchival['name'], 'rb') as f_in:
            with gzip.open(missionArchivePrefix + forArchival['name'] + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                os.remove(f_in.name)

    c.execute('''select * from versions where ''' + toBeDeletedProperty + ''' = 1''', o['origin'])
    toBeDeleted = c.fetchall()
    for deleteMe in toBeDeleted:
        os.remove(missionDirPrefix + deleteMe['name'])

    c.execute("update versions set " + toBeArchivedProperty + " = 0, " + toBeDeletedProperty + " = 0 where " +
              toBeArchivedProperty + " = 1 or " + toBeDeletedProperty + " = 1")
    return
