from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configuration for the tasks application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Task Management'

    def ready(self):
        """
        Override this to perform initialization tasks such as registering signals.
        """
        # Import signals to register them
        import tasks.signals  # noqa
