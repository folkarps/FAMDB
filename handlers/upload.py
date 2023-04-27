import cgi
import pathlib
import shutil
from datetime import date
from urllib.parse import parse_qs

import utils
from handler import Handler


class UploadHandler(Handler):
    def handle(self, environ, start_response):
        params = parse_qs(environ['QUERY_STRING'])
        if environ['REQUEST_METHOD'] != 'POST' or 'missionId' not in params:
            start_response("400 Bad Request", [])
            return ["Must be POST and missionId must be a query parameter".encode()]

        mission_id = params['missionId'][0]
        if not utils.checkUserPermissions(environ['user'], 2, mission_id):
            start_response("403 Permission Denied", [])
            return ["Access Denied".encode()]

        try:
            cgi.maxlen = 20 * 1024 * 1024
            form_data = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                strict_parsing=True,
                keep_blank_values=True
            )
        except (TypeError, ValueError) as e:
            start_response("400 Bad Request", [])
            return [f"File upload error: {e}".encode()]
        if 'upload_file' not in form_data:
            start_response("400 Bad Request", [])
            return ["upload_file must be specified in submitted form".encode()]

        upload_file = form_data['upload_file']
        unsafe_filepath = pathlib.PurePath(upload_file.filename)
        if unsafe_filepath.suffix.lower() != '.pbo':
            start_response("400 Bad Request", [])
            return ["Only .pbo files are allowed".encode()]
        safe_filename = unsafe_filepath.name
        file_data = upload_file.file

        if not utils.is_valid_pbo(file_data):
            start_response("400 Bad Request", [])
            return ["PBO verification failed. Try the upload again".encode()]

        out_path = pathlib.Path(utils.missionMakerDir, safe_filename)
        with out_path.open('wxb') as out_file:
            shutil.copyfileobj(file_data, out_file)

        c = utils.getCursor()
        # rest of the properties are set by defaults in the table
        c.execute(
            "INSERT INTO versions(missionId, name, createDate) VALUES (?, ?, ?)",
            [mission_id, safe_filename, date.today()])
        c.connection.commit()
        c.connection.close()

        start_response("200 OK", [])
        return ["success".encode()]

    def getHandled(self):
        return "upload"
