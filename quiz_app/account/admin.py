from django.contrib import admin

from account.models import (
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', )
    search_fields = ('email', )
