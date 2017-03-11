import random
import string
from urllib.parse import parse_qs

import utils


def handleResetPassword(environ, start_response):
    c = utils.getCursor()
    o = parse_qs(environ['QUERY_STRING'])
    if "email" in o:
        c.execute("select * from users where email = ?", [o['email'][0]])
        user = c.fetchone()
        if user is None:
            start_response("500 Internal Server Response", [])
            return ["No user with this email".encode()]
        else:
            updateLink = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

            c.execute('''update users set resetPwLink = ? where id = ?''', [updateLink, user['id']])

            email = create_msg(
                message_name='FAMDB password reset',
                message_text='To reset your password go to: ' + utils.serverAddress + '/changePassword.html?link=' + updateLink,
                email_from=utils.emailAddress,
                email_to=user['email']
            )
            smtp_server = connect_to_server()
            smtp_server.sendmail(utils.emailAddress, user['email'], email.as_string())
            smtp_server.quit()
            c.connection.commit()
            c.connection.close()
            start_response("200 OK", [])
            return []
    else:
        start_response("500 Internal Server Response", [])
        return ["No email supplied".encode()]


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def connect_to_server():
    server = smtplib.SMTP(utils.emailServer, utils.emailPort)
    server.ehlo()
    server.starttls()
    server.login(utils.emailAddress, utils.emailPassword)
    return server


def create_msg(message_name, message_text, email_from, email_to):
    msg = MIMEMultipart()
    msg['Subject'] = message_name
    msg['From'] = email_from
    msg['To'] = email_to
    msg.attach(MIMEText(message_text, 'html', 'utf-8'))
    return msg
