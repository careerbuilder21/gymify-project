from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email',
                     'first_name', 'role', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
