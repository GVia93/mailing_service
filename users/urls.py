from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ActivateView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    ProfileUpdateView,
    RegisterView, UserListView, UserBlockToggleView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name="password_reset_complete"),
]

urlpatterns += [
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('toggle/<int:pk>/', UserBlockToggleView.as_view(), name='user_toggle_block'),
]