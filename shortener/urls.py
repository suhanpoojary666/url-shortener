from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("shorten/", views.create_short_url),
    path("<str:short_code>/", views.redirect_url),
    path("<str:short_code>/stats/", views.url_stats),
]