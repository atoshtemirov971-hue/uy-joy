from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyatlar'


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.region.name} - {self.name}"

    class Meta:
        verbose_name = 'Tuman'
        verbose_name_plural = 'Tumanlar'


class Listing(models.Model):
    TYPE_CHOICES = (
        ('sale', 'Sotuv'),
        ('rent', 'Ijara'),
        ('daily', 'Kunlik ijara'),
    )
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('inactive', 'Nofaol'),
        ('sold', 'Sotilgan'),
        ('rented', 'Ijarada'),
        ('pending', 'Tekshirilmoqda'),
        ('rejected', 'Rad etilgan'),
    )
    PROPERTY_CHOICES = (
        ('apartment', 'Kvartira'),
        ('house', 'Uy'),
        ('commercial', 'Tijorat'),
        ('land', 'Yer'),
        ('newbuilding', 'Yangi bino'),
    )

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    listing_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_currency = models.CharField(max_length=10, default='UZS')
    is_negotiable = models.BooleanField(default=False)

    area = models.FloatField(help_text='m²')
    rooms = models.IntegerField(default=1)
    floor = models.IntegerField(null=True, blank=True)
    total_floors = models.IntegerField(null=True, blank=True)

    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    is_fake = models.BooleanField(default=False)
    fake_score = models.FloatField(default=0.0)
    views_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'E\'lon'
        verbose_name_plural = 'E\'lonlar'
        ordering = ['-created_at']


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'


class SavedListing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']
        verbose_name = 'Saqlangan e\'lon'
        verbose_name_plural = 'Saqlangan e\'lonlar'


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['listing', 'user']
        verbose_name = 'Sharh'
        verbose_name_plural = 'Sharhlar'