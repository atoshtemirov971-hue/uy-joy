from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search'),
    path('fake-tekshir/<int:listing_id>/', views.fake_check_view, name='fake-check'),
]