from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/create", views.create, name="create"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("watch/<int:listing_id>", views.handleWatch, name="watch"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
]
