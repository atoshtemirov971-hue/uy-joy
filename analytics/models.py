from django.db import models
from accounts.models import CustomUser
from listings.models import Listing


class ListingView(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_views')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ko\'rish'
        verbose_name_plural = 'Ko\'rishlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.listing.title} - {self.created_at}"


class SearchLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=255)
    results_count = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Qidiruv logi'
        verbose_name_plural = 'Qidiruv loglari'
        ordering = ['-created_at']


class SiteStatistics(models.Model):
    date = models.DateField(unique=True)
    total_listings = models.IntegerField(default=0)
    active_listings = models.IntegerField(default=0)
    fake_listings = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_searches = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Sayt statistikasi'
        verbose_name_plural = 'Sayt statistikalari'
        ordering = ['-date']

    def __str__(self):
        return str(self.date)
