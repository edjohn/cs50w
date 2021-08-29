from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Max

from .models import User, Listing, Watchlist, Bid

class BidForm(forms.Form):
    bid = forms.DecimalField(decimal_places=2, min_value=0.01, max_value=10**9, label="", widget=forms.NumberInput(attrs={'class': 'form-control'}))

class ListingForm(forms.Form):
    title = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    price = forms.DecimalField(decimal_places=2, max_digits=19, widget=forms.NumberInput(attrs={'class':'form-control'}))
    url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            watchlist = Watchlist(user=user)
            user.save()
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    bid_form = BidForm()
    listing = Listing.objects.get(id=listing_id)
    item_in_watchlist = False
    max_bid = listing.listing_bids.aggregate(Max('bid'))['bid__max']
    if request.user.is_authenticated:
        watchlist_listings = Watchlist.objects.get(user=request.user).listings
        item_in_watchlist = watchlist_listings.filter(id=listing_id).exists()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": bid_form,
        "item_in_watchlist": item_in_watchlist,
        "max_bid": round(max_bid, 2),
    })
 
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            listing = Listing(title=title, description=description, price=price, url=url, category=category, user=request.user)
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def bid(request, listing_id):
    if request.method == 'POST':
        bid_POST = request.POST["bid"]
        listing = Listing.objects.get(id=listing_id)
        user_bid = Bid(bid=float(bid_POST), user=request.user, listing=listing)
        max_bid = 0
        listing_bids = listing.listing_bids
        if listing_bids.exists():
            max_bid = listing_bids.aggregate(Max('bid'))['bid__max']
        if user_bid.bid >= listing.price and user_bid.bid > max_bid:
            user_bid.save()
        else:
            error_message = "You need a higher bid! Make sure you match the starting bid and exceed the maximum bid."
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

@login_required
def handleWatch(request, listing_id):
    watchlist_listings = Watchlist.objects.get(id=request.user.id).listings
    item_in_watchlist = watchlist_listings.filter(id=listing_id).exists()
    listing = Listing.objects.get(id=listing_id)
    if item_in_watchlist:
        watchlist_listings.remove(listing)
    else:
        watchlist_listings.add(listing)
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))