from . import mail
from flask_mail import Message
from flask import current_app

TEMPLATE_PATH = "./common/email/template/"
EMAIL_HTML = {
    "code": TEMPLATE_PATH + "code.html"
}


def send_email(app, email, title, template, **context):
    with app.app_context():
        if template not in EMAIL_HTML.keys():
            return None
        with open(EMAIL_HTML[template], 'r', encoding="utf-8") as f:
            html = f.read()
            msg = Message(
                current_app.config['MAIL_SUBJECT_PREFIX'] + '-%s' % title,
                sender=current_app.config['MAIL_SENDER'],
                recipients=[email],
                html=html.format(**context)
            )
            mail.send(msg)



