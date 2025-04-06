from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import register, login_view, logout_view, profile

app_name = "accounts"


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("account:password_change_done"),
            template_name="password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change_done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
]
