from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("about", views.about, name="about"),
    path("login", views.login_page, name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]