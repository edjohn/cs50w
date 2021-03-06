from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/create", views.create, name="create"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
]
