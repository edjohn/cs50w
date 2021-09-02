from django.contrib import admin
from .models import Category, User, Bid, Listing, Comment, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Category)