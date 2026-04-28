from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FaceLogin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'role', 'is_verified', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_staff']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('phone', 'avatar', 'role', 'bio', 'is_verified', 'face_encoding')
        }),
    )


@admin.register(FaceLogin)
class FaceLoginAdmin(admin.ModelAdmin):
    list_display = ['user', 'success', 'created_at']
    list_filter = ['success']
    search_fields = ['user__username']
    ordering = ['-created_at']