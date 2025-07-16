from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, CustomPasswordResetView, \
    CustomPasswordResetConfirmView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
