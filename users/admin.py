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
        readonly_fields = list()

        # If the user is not superuser
        if not request.user.is_superuser:
            readonly_fields += ['is_superuser'] # Not able to change superuser status

            # If the object is not null and not your own user
            if obj and obj != auth.get_user(request):
                readonly_fields += ['email', 'username'] # Not able to change username

                # If the object is superuser
                if obj.is_superuser:
                    readonly_fields += ['first_name', 'last_name',
                                        'gender', 'address',
                                        'phone_number', 'is_staff',
                                        'is_active', 'groups',] # Not able to change anything

        return readonly_fields

admin.site.register(User, CustomUserAdmin)
