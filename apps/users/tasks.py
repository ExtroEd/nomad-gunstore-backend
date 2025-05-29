from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os


@shared_task
def send_verification_email(email, code):
    subject = 'Подтверждение Email — Nomad Tactical'

    context = {
        'email': email,
        'code': code,
        'logo_url': os.getenv('LOGO_URL')
    }

    html_message = render_to_string(
        'emails/verification_email.html', context
    )

    plain_message = (
        f"Nomad Tactical\n\n"
        f"Компания Nomad Tactical получила запрос на подтверждение адреса "
        f"электронной почты {email}.\n\n"
        f"Используйте этот код для подтверждения:\n\n"
        f"{code}\n\n"
        f"Срок действия кода истекает через 24 часа.\n\n"
        f"Если вы не запрашивали этот код, просто проигнорируйте это письмо.\n"
    )

    msg = EmailMultiAlternatives(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()


@shared_task
def clear_verification_code(user_id):
    from .models import CustomUser
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.verification_code = None
        user.save()
    except CustomUser.DoesNotExist:
        pass
