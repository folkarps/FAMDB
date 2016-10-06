from pathlib import Path
from shutil import copyfileobj
from urllib.parse import urlparse, parse_qs

import utils


def handleMove(request):
    o = parse_qs(urlparse(request.path).query)
    fileName = o['name']
    if (Path(utils.missionMakerDir + fileName).is_file()):
        copyfileobj(utils.missionMakerDir + fileName, utils.missionMainDir + fileName)

    return
