from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import json
from .models import Payment, PremiumSubscription
from listings.models import Listing


@login_required
def payment_list_view(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payments/list.html', {'payments': payments})


@login_required
def featured_listing_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
    if request.method == 'POST':
        provider = request.POST.get('provider', 'payme')
        payment = Payment.objects.create(
            user=request.user,
            listing=listing,
            amount=50000,
            payment_type='featured',
            provider=provider,
            status='success'
        )
        listing.is_featured = True
        listing.save()
        messages.success(request, 'E\'lon ko\'tarildi!')
        return redirect('listing-detail', slug=listing.slug)
    return render(request, 'payments/featured.html', {'listing': listing})


@login_required
def premium_subscription_view(request):
    if request.method == 'POST':
        provider = request.POST.get('provider', 'payme')
        payment = Payment.objects.create(
            user=request.user,
            amount=100000,
            payment_type='premium',
            provider=provider,
            status='success'
        )
        PremiumSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                'payment': payment,
                'expires_at': timezone.now() + timedelta(days=30),
                'is_active': True
            }
        )
        messages.success(request, 'Premium obuna faollashtirildi!')
        return redirect('profile')
    return render(request, 'payments/premium.html')


@csrf_exempt
def payme_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        if transaction_id and status == 'success':
            Payment.objects.filter(
                transaction_id=transaction_id
            ).update(status='success')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
def click_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        if transaction_id and status == 'success':
            Payment.objects.filter(
                transaction_id=transaction_id
            ).update(status='success')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid method'}, status=405)
