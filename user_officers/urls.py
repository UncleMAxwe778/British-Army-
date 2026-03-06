from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, profile_edit, profile_view


app_name = 'auth_officers'


urlpatterns = [
    path('register-page/', register_view, name='register_view'),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("profile/", profile_view, name="profile_view"),
    path("login/", LoginView.as_view(template_name="user_officers/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]