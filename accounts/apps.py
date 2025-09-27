from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'User Accounts'

    def ready(self):
        """
        Override this to perform initialization tasks such as registering signals.
        """
        # Import signals to register them
        import accounts.signals  # noqa
