from io import StringIO

from drf.settings.base import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMessage


def send_mail_with_attachment(subject: str, to_mail, attachment: StringIO, attachment_name: str, attachment_type: str):
    email = EmailMessage(
        subject=subject,
        from_email=DEFAULT_FROM_EMAIL,
        to=to_mail, 
    )

    email.attach(attachment_name, attachment.getvalue(), attachment_type)
    email.send()