from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing
from accounts.models import CustomUser
from .models import ListingView, SearchLog, SiteStatistics


@login_required
def dashboard_view(request):
    user = request.user
    my_listings = Listing.objects.filter(owner=user)
    total_views = sum(l.views_count for l in my_listings)
    active_listings = my_listings.filter(status='active').count()
    pending_listings = my_listings.filter(status='pending').count()
    fake_listings = my_listings.filter(is_fake=True).count()

    last_30_days = timezone.now() - timedelta(days=30)
    recent_views = ListingView.objects.filter(
        listing__owner=user,
        created_at__gte=last_30_days
    ).count()

    context = {
        'my_listings': my_listings,
        'total_views': total_views,
        'active_listings': active_listings,
        'pending_listings': pending_listings,
        'fake_listings': fake_listings,
        'recent_views': recent_views,
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def admin_statistics_view(request):
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()

    total_listings = Listing.objects.count()
    active_listings = Listing.objects.filter(status='active').count()
    fake_listings = Listing.objects.filter(is_fake=True).count()
    total_users = CustomUser.objects.count()

    last_7_days = timezone.now() - timedelta(days=7)
    new_users = CustomUser.objects.filter(date_joined__gte=last_7_days).count()
    new_listings = Listing.objects.filter(created_at__gte=last_7_days).count()

    top_listings = Listing.objects.filter(
        status='active'
    ).order_by('-views_count')[:10]

    context = {
        'total_listings': total_listings,
        'active_listings': active_listings,
        'fake_listings': fake_listings,
        'total_users': total_users,
        'new_users': new_users,
        'new_listings': new_listings,
        'top_listings': top_listings,
    }
    return render(request, 'analytics/statistics.html', context)