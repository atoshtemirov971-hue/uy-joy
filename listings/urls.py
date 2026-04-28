from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('e-lonlar/', views.listing_list_view, name='listing-list'),
    path('e-lonlar/yangi/', views.listing_create_view, name='listing-create'),
    path('e-lonlar/mening/', views.my_listings_view, name='my-listings'),
    path('e-lonlar/<slug:slug>/', views.listing_detail_view, name='listing-detail'),
    path('e-lonlar/<slug:slug>/tahrirlash/', views.listing_edit_view, name='listing-edit'),
    path('e-lonlar/<slug:slug>/ochirish/', views.listing_delete_view, name='listing-delete'),
    path('e-lonlar/<slug:slug>/saqlash/', views.save_listing_view, name='listing-save'),
]