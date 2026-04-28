from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, FaceLoginView, FaceRegisterView, RegisterAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('face-login/', FaceLoginView.as_view(), name='api-face-login'),
    path('face-register/', FaceRegisterView.as_view(), name='api-face-register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]