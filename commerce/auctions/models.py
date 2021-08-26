from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19)
    url = models.URLField(default='')
    category = models.CharField(max_length=80, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings", default='')

    def __str__(self):
        return f"{self.title} : {self.description} : ${self.price}"

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=19)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", default='')

    def __str__(self):
        return f"${self.bid}"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default='')

    def __str__(self):
        return f"{self.user} : {self.comment}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True, related_name="listing_watchlists")

    def __str__(self):
        return f'{self.user} : {str(self.listings)}'