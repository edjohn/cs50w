from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BooleanField

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category = models.CharField(max_length=80, unique=True, default='')

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    url = models.URLField(default='', blank=True, null=True)
    category = models.CharField(max_length=80, default='', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    active = BooleanField(default=True)
    winner = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name="user_wins")

    def __str__(self):
        return f"{self.title} : {self.description} : ${self.price}"

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=9)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", default='')

    def __str__(self):
        return f"${self.bid} on {self.listing} by {self.user}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default='')

    def __str__(self):
        return f"{self.user} : {self.comment}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="listing_watchlists")

    def __str__(self):
        return f'{self.user} : {str(self.listings)}'