from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listingID>", views.listing, name="listing"),
    path("watch", views.watch, name="watch"),
    path("categories", views.category, name="category"),
    path("add_watchlist/<int:listingID>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listingID>", views.remove_watchlist, name="remove_watchlist"),
    path("close_listing/<int:listingID>", views.close_listing, name="close_listing")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)