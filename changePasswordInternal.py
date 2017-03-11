import json

from passlib.hash import sha256_crypt

import utils


def handleChangePassword(environ, start_response):
    changePasswordString = utils.environToContents(environ)
    changePasswordJson = json.loads(changePasswordString)

    c = utils.getCursor()
    c.execute("select * from users where resetPwLink = ?", [changePasswordJson['link']])
    userRow = c.fetchone()
    if userRow is None:
        start_response("500 internal server error", [])
        return ["Unable to find user with this link, try reset password again".encode()]
    else:
        c.execute('''update users set password = ?, resetPwLink = null where id = ?''',
                  [sha256_crypt.encrypt(changePasswordJson['password']), userRow['id']])
        c.connection.commit()
        c.connection.close()
        start_response("200 OK", [])
        return []
