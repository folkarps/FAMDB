import json

from passlib.hash import sha256_crypt

import utils
from handler import Handler


class ChangePasswordInternal(Handler):
    def handle(self, environ, start_response):
        changePasswordString = utils.environToContents(environ)
        changePasswordJson = json.loads(changePasswordString)

        c = utils.getCursor()
        c.execute("SELECT * FROM users WHERE resetPwLink = ?", [changePasswordJson['link']])
        userRow = c.fetchone()
        if userRow is None:
            start_response("500 internal server error", [])
            return ["Unable to find user with this link, try reset password again".encode()]
        else:
            c.execute('''UPDATE users SET password = ?, resetPwLink = NULL WHERE id = ?''',
                      [sha256_crypt.encrypt(changePasswordJson['password']), userRow['id']])
            c.connection.commit()
            c.connection.close()
            start_response("200 OK", [])
            return []

    def getHandled(self):
        return "changePasswordInternal"
