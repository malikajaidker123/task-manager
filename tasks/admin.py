from django.contrib import admin
from django.utils.html import format_html
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # ""
    # Admin interface for the Task model.
    # """
    list_display = ('title', 'owner_email', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__email')
    readonly_fields = ('created_at', 'updated_at', 'owner')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Metadata', {
            'fields': ('owner', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def owner_email(self, obj):
        return obj.owner.email
    owner_email.short_description = 'Owner Email'
    owner_email.admin_order_field = 'owner__email'

    def get_queryset(self, request):
        # ""
        # Filter the tasks to only show those owned by the current user,
        # unless the user is a superuser.
        # """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        # ""
        # Set the task owner to the current user when creating a new task.
        # """
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
