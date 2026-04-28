from django.contrib import admin
from .models import Payment, PremiumSubscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'currency', 'status', 'payment_type', 'provider', 'created_at']
    list_filter = ['status', 'payment_type', 'provider']
    search_fields = ['user__username', 'transaction_id']
    ordering = ['-created_at']


@admin.register(PremiumSubscription)
class PremiumSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'started_at', 'expires_at']
    list_filter = ['is_active']
    ordering = ['-started_at']