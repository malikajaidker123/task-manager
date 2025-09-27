from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    """Admin interface for the custom User model."""
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # ""
        # Make email read-only for non-superusers when editing an existing user.
        # """
        if not request.user.is_superuser:
            return self.readonly_fields + ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        return self.readonly_fields

    def get_queryset(self, request):
        # ""
        # Filter users to only show those created by the current user,
        # unless the user is a superuser.
        # """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def has_delete_permission(self, request, obj=None):
        ""
        # Only allow superusers to delete users.
        # """
        # return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # ""
        # Allow users to edit their own profile.
        # """
        if obj is None:
            return True
        return obj == request.user or request.user.is_superuser

# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
