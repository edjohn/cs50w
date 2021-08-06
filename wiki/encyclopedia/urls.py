from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:title>", views.entry, name="entry")
]