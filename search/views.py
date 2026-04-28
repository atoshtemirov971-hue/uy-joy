from django.shortcuts import render
from django.db.models import Q
from listings.models import Listing, Category, Region
from .ml_detector import FakeListingDetector

detector = FakeListingDetector()


def search_view(request):
    query = request.GET.get('q', '')
    listing_type = request.GET.get('type', '')
    property_type = request.GET.get('property_type', '')
    region = request.GET.get('region', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    rooms = request.GET.get('rooms', '')
    ordering = request.GET.get('ordering', '-created_at')

    listings = Listing.objects.filter(status='active', is_fake=False)

    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )
    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    if property_type:
        listings = listings.filter(property_type=property_type)
    if region:
        listings = listings.filter(region__slug=region)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if rooms:
        listings = listings.filter(rooms=rooms)

    listings = listings.order_by(ordering)

    context = {
        'listings': listings,
        'query': query,
        'categories': Category.objects.all(),
        'regions': Region.objects.all(),
        'total': listings.count(),
    }
    return render(request, 'search/results.html', context)


def fake_check_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    result = detector.predict(listing)
    listing.is_fake = result['is_fake']
    listing.fake_score = result['score']
    listing.save()
    return render(request, 'search/fake_result.html', {'result': result, 'listing': listing})