
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Task

@receiver(pre_save, sender=Task)
def update_task_timestamps(sender, instance, **kwargs):
    instance.updated_at = timezone.now()

@receiver(post_save, sender=Task)
def task_created_notification(sender, instance, created, **kwargs):
    """
    Send a notification when a new task is created.
    """
    if created:
        # In a real application, you might want to send an email or notification here
        print(f"New task created: {instance.title}")  # For demonstration purposes
