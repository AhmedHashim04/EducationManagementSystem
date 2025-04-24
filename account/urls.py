
from django.contrib import admin
from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views

from .views import Register, ProfileView
app_name = 'account'

urlpatterns = [
    path('register/',Register.as_view(),name='register'),
    path('login/',views.LoginView.as_view(template_name='account/login.html'),name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('password_change/',views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 


