import logging
from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_mail(title, email_plaintext_message, email_html_message, receivers):
    msg = EmailMultiAlternatives(
        title,
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        receivers
    )
    msg.attach_alternative(email_html_message, "text/html")
    try:
        msg.send()
    except SMTPAuthenticationError:
        logging.exception(f"SMTPAuthenticationError - Error sending mail to {receivers}")
    except Exception:
        logging.exception("Exception - Error sending mail to {receivers}")
