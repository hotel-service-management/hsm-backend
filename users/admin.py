from django.contrib import admin
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
    list_display = ['email', 'username', 'first_name', 'last_name', ]

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password',)
            }
        ),
        (
            'Personal Info', {
                'fields': ('first_name', 'last_name', 'gender', 'address',)
            }
        ),
        (
            'Permissions', {
                'fields': ('is_staff', 'is_active',)
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
                'fields': (
                    'first_name', 'last_name', 'gender', 'address',
                )
            }
        ),
        (
            'Permission',
            {
                'fields': ('is_staff', 'is_active')
            }
        ),
        (
            'Dangerous Zone', {
                'fields': ('is_superuser',),
            }
        ),
    )


admin.site.register(User, CustomUserAdmin)
