from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Listing, ListingImage, SavedListing, Category, Region, District, Review
from .serializers import ListingSerializer, ListingDetailSerializer, ReviewSerializer


def home_view(request):
    featured = Listing.objects.filter(status='active', is_featured=True)[:6]
    latest = Listing.objects.filter(status='active')[:12]
    categories = Category.objects.all()
    regions = Region.objects.all()
    context = {
        'featured': featured,
        'latest': latest,
        'categories': categories,
        'regions': regions,
    }
    return render(request, 'listings/home.html', context)


def listing_list_view(request):
    listings = Listing.objects.filter(status='active', is_fake=False)
    listing_type = request.GET.get('type')
    category = request.GET.get('category')
    region = request.GET.get('region')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rooms = request.GET.get('rooms')

    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    if category:
        listings = listings.filter(category__slug=category)
    if region:
        listings = listings.filter(region__slug=region)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if rooms:
        listings = listings.filter(rooms=rooms)

    paginator = Paginator(listings, 12)
    page = request.GET.get('page')
    listings = paginator.get_page(page)

    context = {
        'listings': listings,
        'categories': Category.objects.all(),
        'regions': Region.objects.all(),
    }
    return render(request, 'listings/list.html', context)


def listing_detail_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug, status='active')
    listing.views_count += 1
    listing.save()
    similar = Listing.objects.filter(
        region=listing.region,
        status='active'
    ).exclude(id=listing.id)[:4]
    reviews = listing.reviews.all()
    context = {
        'listing': listing,
        'similar': similar,
        'reviews': reviews,
    }
    return render(request, 'listings/detail.html', context)


@login_required
def listing_create_view(request):
    if request.method == 'POST':
        from .forms import ListingForm
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_main=(i == 0)
                )
            messages.success(request, 'E\'lon muvaffaqiyatli yaratildi!')
            return redirect('listing-detail', slug=listing.slug)
    else:
        from .forms import ListingForm
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})


@login_required
def listing_edit_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    if request.method == 'POST':
        from .forms import ListingForm
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'E\'lon yangilandi!')
            return redirect('listing-detail', slug=listing.slug)
    else:
        from .forms import ListingForm
        form = ListingForm(instance=listing)
    return render(request, 'listings/edit.html', {'form': form, 'listing': listing})


@login_required
def listing_delete_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'E\'lon o\'chirildi!')
        return redirect('listing-list')
    return render(request, 'listings/delete.html', {'listing': listing})


@login_required
def save_listing_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    saved, created = SavedListing.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    if not created:
        saved.delete()
        messages.info(request, 'E\'lon saqlanganlardan olib tashlandi')
    else:
        messages.success(request, 'E\'lon saqlandi!')
    return redirect('listing-detail', slug=slug)


@login_required
def my_listings_view(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.filter(status='active', is_fake=False)
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['listing_type', 'property_type', 'region', 'rooms']
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['price', 'created_at', 'views_count']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ListingDetailSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def save_listing(self, request, pk=None):
        listing = self.get_object()
        saved, created = SavedListing.objects.get_or_create(
            user=request.user, listing=listing
        )
        if not created:
            saved.delete()
            return Response({'status': 'removed'})
        return Response({'status': 'saved'})
