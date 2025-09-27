"""
Signals for the accounts app.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send a welcome email to new users when they register.
    """
    if created and instance.email:
        subject = 'Welcome to Task Manager'
        html_message = render_to_string('emails/welcome_email.html', {
            'user': instance,
            'site_name': 'Task Manager'
        })
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [instance.email]
        
        send_mail(
            subject,
            plain_message,
            from_email,
            to,
            html_message=html_message,
            fail_silently=True
        )

@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    """
    Handle user pre-save operations.
    """
    # Ensure email is always lowercase
    if instance.email:
        instance.email = instance.email.lower()
    
    # If this is a new user, set the username to be the same as email
    if not instance.pk and not instance.username:
        instance.username = instance.email
