from rest_framework import serializers
from .models import Listing, ListingImage, Category, Region, District, Review
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'slug']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'slug', 'region']


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'is_main', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'slug', 'description',
            'listing_type', 'property_type', 'status',
            'price', 'price_currency', 'is_negotiable',
            'area', 'rooms', 'floor', 'total_floors',
            'address', 'latitude', 'longitude',
            'region', 'region_name', 'district', 'district_name',
            'category', 'category_name',
            'images', 'views_count', 'is_featured',
            'is_fake', 'fake_score',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'is_fake', 'fake_score', 'created_at', 'updated_at']


class ListingDetailSerializer(ListingSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + ['reviews']