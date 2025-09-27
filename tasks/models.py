from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Task(models.Model):
    """
    Task model to store task information.
    """
    title = models.CharField(max_length=200, help_text="Title of the task")
    description = models.TextField(blank=True, help_text="Detailed description of the task")
    completed = models.BooleanField(default=False, help_text="Whether the task is completed")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the task was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the task was last updated")
    owner = models.ForeignKey(
        User, 
        related_name='tasks',
        on_delete=models.CASCADE,
        help_text="The user who owns this task"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Pending'}"

    def save(self, *args, **kwargs):
        """Override save to update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
