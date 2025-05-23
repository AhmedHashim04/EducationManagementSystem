
from django.urls import path, include
from .views import ChangePasswordView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterAPIView, ProfileView
app_name = 'account'

urlpatterns = [
    
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('password_change/',ChangePasswordView.as_view(),name='password_change'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] 


