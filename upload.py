import os
import re
from datetime import date
from urllib.parse import parse_qs

import utils


def handleUpload(environ, start_response):
    c = utils.getCursor()
    o = parse_qs(environ['QUERY_STRING'])
    missionId = o['missionId'][0]
    if not utils.checkUserPermissions(environ['user'], 2, missionId):
        start_response("403 Permission Denied", [])
        return ["Access Denied"]

    # This monstrosity of code was copied from the internet, I barely understand how it works

    content_type = environ.get('CONTENT_TYPE', '0')
    if not content_type:
        start_response("500 Internal Server Error", [])
        return ["Content-Type header doesn't contain boundary".encode()]
    boundary = content_type.split("=")[1].encode()
    remainbytes = int(environ.get('CONTENT_LENGTH', '0'))

    if remainbytes > (20 * 1024):
        start_response("500 Internal Server Error", [])
        return ["20 MB is the max size".encode()]


    line = environ['wsgi.input'].readline()
    remainbytes -= len(line)
    if not boundary in line:
        start_response("500 Internal Server Error", [])
        return ["Content NOT begin with boundary".encode()]
    line = environ['wsgi.input'].readline()
    remainbytes -= len(line)
    decode = line.decode()
    regex = r'Content-Disposition.*name="upload_file"; filename="(.*)".*'
    fn = re.findall(regex, decode)
    if not fn:
        start_response("500 Internal Server Error", [])
        return ["Can't find out file name...".encode()]

    fileName = fn[0]

    # protect from filesystem roaming
    fileName = fileName.replace("..", "")

    if not fileName.endswith(".pbo"):
        start_response("500 Internal Server Error", [])
        return ["Only .pbo files are allowed".encode()]


    fullPath = os.path.join(utils.missionMakerDir, fileName).replace("\n", "")
    line = environ['wsgi.input'].readline()
    remainbytes -= len(line)
    line = environ['wsgi.input'].readline()
    remainbytes -= len(line)
    try:
        out = open(fullPath, 'wb')
    except IOError:
        start_response("500 Internal Server Error", [])
        return ["Can't create file to write, do you have permission to write?".encode()]

    preline = environ['wsgi.input'].readline()
    remainbytes -= len(preline)
    while remainbytes > 0:
        line = environ['wsgi.input'].readline()
        remainbytes -= len(line)
        if boundary in line:
            preline = preline[0:-1]
            if preline.endswith(b'\r'):
                preline = preline[0:-1]
            out.write(preline)
            out.close()
        else:
            out.write(preline)
            preline = line
    # rest of the properties are set by defaults in the table
    c.execute(
        "insert into versions(missionId, name, createDate) values (?, ?, ?)",
        [missionId, fileName, date.today()])
    c.connection.commit()
    c.connection.close()

    start_response("200 OK", [])
    return ["success".encode()]
