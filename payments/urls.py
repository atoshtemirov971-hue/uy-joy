from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list_view, name='payment-list'),
    path('premium/', views.premium_subscription_view, name='premium'),
    path('elon-kotarish/<int:listing_id>/', views.featured_listing_view, name='featured-listing'),
    path('webhook/payme/', views.payme_webhook, name='payme-webhook'),
    path('webhook/click/', views.click_webhook, name='click-webhook'),
]