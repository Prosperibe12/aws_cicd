from django.contrib import admin
from django_cicd import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phoneNumber',
        'city',
        'user_type',
        'is_verified',
        'is_updated',
        'is_active',
        'created_at'
    )


admin.site.register(models.User, UserAdmin)
