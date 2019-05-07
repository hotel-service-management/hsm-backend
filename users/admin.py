from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from .forms import UserCreationForm, UserChangeForm
from .models import User

# Add permission
admin.site.register(Permission)


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name']

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'username', 'password')
            }
        ),
        (
            'Personal Info', {
                'fields': ('first_name', 'last_name', 'gender', 'address', 'phone_number')
            }
        ),
        (
            'Permissions', {
                'fields': ('is_staff', 'is_active', 'groups')
            }
        ),
        (
            'Dangerous Zone', {
                'fields': ('is_superuser',),
                'classes': ('collapse',)
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'username', 'email', 'password1', 'password2',
                )
            },

        ),
        (
            'Personal Info',
            {
                'fields': ('first_name', 'last_name', 'gender', 'address', 'phone_number')
            }
        ),
        (
            'Permission',
            {
                'fields': ('is_staff', 'is_active', 'groups')
            }
        ),
        (
            'Dangerous Zone', {
                'fields': ('is_superuser',),
            }
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        # If is not superuser, can only edit own username. Also, must have permission `change_user`.
        if not request.user.is_superuser and obj != auth.get_user(request):
            return ['username']
        return []


admin.site.register(User, CustomUserAdmin)
