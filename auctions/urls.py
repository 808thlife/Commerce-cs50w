from django.urls import path
from django.conf.urls.static import static, settings
import os

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categoriesPage, name = "categories"),
    path("add/", views.add, name = "add"),
    path("listing/<int:itemID>", views.viewListing, name = "listing"),
    #path("listing/<int:itemID>/accept", views.acceptBid, name = "accept")
    path("categories/<str:catTitle>/<int:catID>", views.watchCat, name = "watchCategory"),
    path("watchlist", views.watchlist, name = "watchlist")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
