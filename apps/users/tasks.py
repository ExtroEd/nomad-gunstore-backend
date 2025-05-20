from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(email, code):
    subject = 'Подтверждение Email — Nomad Tactical'
    message = (
        f"Nomad Tactical\n\n"
        f"Компания Nomad Tactical получила запрос на подтверждение адреса "
        f"электронной почты {email}.\n\n"
        f"Используйте этот код для подтверждения:\n\n"
        f"{code}\n\n"
        f"Срок действия кода истекает через 24 часа.\n\n"
        f"Если вы не запрашивали этот код, просто проигнорируйте это письмо.\n"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@shared_task
def clear_verification_code(user_id):
    from .models import CustomUser
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.verification_code = None
        user.save()
    except CustomUser.DoesNotExist:
        pass
