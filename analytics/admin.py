from django.contrib import admin
from .models import ListingView, SearchLog, SiteStatistics


@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'results_count', 'created_at']
    ordering = ['-created_at']


@admin.register(SiteStatistics)
class SiteStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_listings', 'active_listings', 'fake_listings', 'total_users', 'new_users']
    ordering = ['-date']
