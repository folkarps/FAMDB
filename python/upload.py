import os
import re
from datetime import date
from urllib.parse import urlparse, parse_qs

import utils


def handleUpload(request):
    c = utils.getCursor()
    o = parse_qs(urlparse(request.path).query)
    content_type = request.headers['content-type']
    if not content_type:
        request.wfile.write("Content-Type header doesn't contain boundary".encode())
    boundary = content_type.split("=")[1].encode()
    remainbytes = int(request.headers['content-length'])
    line = request.rfile.readline()
    remainbytes -= len(line)
    if not boundary in line:
        request.wfile.write("Content NOT begin with boundary".encode())
    line = request.rfile.readline()
    remainbytes -= len(line)
    decode = line.decode()
    regex = r'Content-Disposition.*name="upload_file"; filename="(.*)".*'
    fn = re.findall(regex, decode)
    if not fn:
        request.wfile.write("Can't find out file name...")
    fileName = fn[0]
    fullPath = os.path.join(utils.missionMakerDir, fileName).replace("\n", "")
    line = request.rfile.readline()
    remainbytes -= len(line)
    line = request.rfile.readline()
    remainbytes -= len(line)
    try:
        out = open(fullPath, 'wb')
    except IOError:
        request.wfile.write("Can't create file to write, do you have permission to write?".encode())

    preline = request.rfile.readline()
    remainbytes -= len(preline)
    while remainbytes > 0:
        line = request.rfile.readline()
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
    request.wfile.write("success".encode())
    c.execute(
        "insert into versions(origin, missionId, name, createDate, toBeArchived, toBeDeleted) values (?, ?, ?, ?, ?, ?)",
        ['missionMaking', o['missionId'][0], fileName, date.today(), 0, 0])
    c.connection.commit()
    c.connection.close()
    return
