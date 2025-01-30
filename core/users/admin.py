from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'email_verified', 'date_joined')
    list_filter = ('is_active', 'email_verified', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_verified', 'is_expired')
    list_filter = ('verified_at',)
    search_fields = ('user__username', 'user__email', 'token')
    ordering = ('-created_at',)
    readonly_fields = ('token', 'created_at')
