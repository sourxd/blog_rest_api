from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Blog

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)