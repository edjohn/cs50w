from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import SET_DEFAULT, SET_NULL
from django.db.models.fields import BooleanField, related

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19)
    url = models.URLField(default='')
    category = models.CharField(max_length=80, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    active = BooleanField(default=True)
    winner = models.OneToOneField(User, default=None, blank=True, null=True, on_delete=SET_NULL)

    def setActive(self):
        self.active = True

    def setInactive(self):
        self.active = False
    
    def setWinner(self, winner):
        self.winner = winner

    def __str__(self):
        return f"{self.title} : {self.description} : ${self.price}"

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=19)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", default='')

    def __str__(self):
        return f"${self.bid} on {self.listing}"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default='')

    def __str__(self):
        return f"{self.user} : {self.comment}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="listing_watchlists")

    def __str__(self):
        return f'{self.user} : {str(self.listings)}'