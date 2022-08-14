from django.urls import path
from . import views
urlpatterns = [
    path("", views.homepage, name="home"),
    path("about", views.about, name="about"),
    path("login", views.login_page, name="login"),

]