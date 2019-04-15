from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Permission

# Add permission
admin.site.register(Permission)


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username', ]

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
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'password1', 'password2',
                )
            },

        ),
        (
            'Personal Info',
            {
                'classes': ('wide',),
                'fields': (
                    'first_name', 'last_name', 'gender', 'address',
                )
            }
        ),
        (
            'Permission',
            {
                'classes': ('wide',),
                'fields': ('is_staff', 'is_active')
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
