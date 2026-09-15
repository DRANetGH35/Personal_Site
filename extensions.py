from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase
import os
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid, formatdate
import smtplib

EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

class Base(DeclarativeBase):
    pass

from sqlalchemy import MetaData
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base.metadata.naming_convention = naming_convention

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
bootstrap = Bootstrap5()

def send_verification_email(code, address):
    my_email = "messenger@dradigital.net"

    msg = MIMEText(f"Your verification code is {code}")
    msg["Subject"] = "DRADigital Account Verification"
    msg["From"] = formataddr(("DRADigital", my_email))
    msg["To"] = address
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dradigital.net")

    with smtplib.SMTP("mail.dradigital.net", 587, timeout=20) as server:
        server.starttls()
        server.login(my_email, EMAIL_PASSWORD)
        server.sendmail(my_email, [msg["To"]], msg.as_string())


def send_reset_link(link, address):
    my_email = "messenger@dradigital.net"

    msg = MIMEText(f"To reset you password, visit the following link \n {link} \n\n If you did not request a password reset, please ignore this email")
    msg["Subject"] = "DRADigital Password Reset"
    msg["From"] = formataddr(("DRADigital", my_email))
    msg["To"] = address
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dradigital.net")

    with smtplib.SMTP("mail.dradigital.net", 587, timeout=20) as server:
        server.starttls()
        server.login(my_email, EMAIL_PASSWORD)
        server.sendmail(my_email, [msg["To"]], msg.as_string())