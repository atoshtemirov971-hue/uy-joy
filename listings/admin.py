from django.contrib import admin
from .models import Listing, ListingImage, Category, Region, District, SavedListing, Review


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 3


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'listing_type', 'property_type', 'price', 'status', 'is_fake', 'created_at']
    list_filter = ['listing_type', 'property_type', 'status', 'is_fake', 'is_featured']
    search_fields = ['title', 'description', 'address']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ListingImageInline]
    readonly_fields = ['views_count', 'fake_score', 'created_at', 'updated_at']

    actions = ['mark_as_active', 'mark_as_fake']

    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, 'E\'lonlar faollashtirildi!')
    mark_as_active.short_description = 'Faollashtirish'

    def mark_as_fake(self, request, queryset):
        queryset.update(is_fake=True, status='rejected')
        self.message_user(request, 'E\'lonlar soxta deb belgilandi!')
    mark_as_fake.short_description = 'Soxta deb belgilash'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'slug']
    list_filter = ['region']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
    ordering = ['-created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    ordering = ['-created_at']
