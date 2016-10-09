from pathlib import Path
from shutil import copyfileobj
from urllib.parse import urlparse, parse_qs

import utils


def handleMove(request):
    o = parse_qs(urlparse(request.path).query)
    user = utils.getCurrentUser(request)
    missionId = o['missionId']
    # If you're a MM user and this is your mission, or you're a low admin
    if not (utils.checkUserPermissions(user, 1, missionId=missionId, collector=utils.AND) or utils.checkUserPermissions(
            user, 2)):
        request.wfile.write("Access Denied".encode())
        return

    fileName = o['name']
    if (Path(utils.missionMakerDir + fileName).is_file()):
        copyfileobj(utils.missionMakerDir + fileName, utils.missionMainDir + fileName)

    return
