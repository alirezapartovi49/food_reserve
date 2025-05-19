from django.db.models.signals import post_save
from django.dispatch import receiver

from auth.tasks import send_verifiacation_mail
from auth.services import generate_otp_code
from .models import User, VerificationCode


@receiver(post_save, sender=User)
def send_verification_code(sender, instance: User, created: bool, **kwargs):
    if created:
        code = generate_otp_code()
        VerificationCode.objects.create(user=instance, code=code)
        send_verifiacation_mail(to=instance.email, code=code)
