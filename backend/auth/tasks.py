from smtplib import SMTPException
from typing import NewType, List
from threading import Thread

from django.core.mail import send_mail
from django.conf import settings


EMAIL_TYPE = NewType("EMAIL_TYPE", str)


def send_email(data: dict):
    try:
        send_mail(**data)
    except SMTPException as e:
        print(f"send email is failed with this data {data}\n{e}")


def send_verifiacation_mail(to: EMAIL_TYPE | List, code: int):
    data = {
        "subject": "ferez verification code",
        "message": f"<h4>your verification code for ferezi</h4><br/><h2>{code}</h2>",
        "from_email": settings.FEREZI_EMAIL,
        "recipient_list": [to],
        # "fail_silently": True,
    }
    task = Thread(target=send_email, args=(data,))
    task.start()
