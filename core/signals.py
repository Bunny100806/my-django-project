from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Post
from .tasks import send_post_notification

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        send_post_notification.delay(instance.id)

