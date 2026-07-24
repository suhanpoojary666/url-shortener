from django.urls import path
from . import views

urlpatterns = [
    path('myurls/',views.my_urls),                              #all the specified end points must be defined before <str:short_code> as it will accept any endpoint request
    path("register/", views.register),
    path("shorten/", views.create_short_url),
    path("<str:short_code>/stats/", views.url_stats),
    path("<str:short_code>/", views.redirect_url),
    path("<str:short_code>/delete/",views.delete_url),
    path("<str:short_code>/update/",views.update_url),
]