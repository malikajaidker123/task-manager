from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractUser):
    """
    Custom user model that uses email as the unique identifier
    instead of username.
    """
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Must be a valid email address.')
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        help_text=_('Optional. 150 characters or fewer.')
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        help_text=_('Optional. 150 characters or fewer.')
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        # ""Return the short name for the user."""
        return self.first_name
