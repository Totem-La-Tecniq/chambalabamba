from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_thank_you_email(donacion):
    subject = "¡Gracias por tu donación!"
    message = render_to_string("donaciones/thank_you_email.txt", {"donacion": donacion})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [donacion.email]
    send_mail(subject, message, from_email, recipient_list)
