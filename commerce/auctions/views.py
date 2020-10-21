from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment, Watch


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bids": Bid.objects.all()
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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def listing(request, listing_id):
    if request.method == "POST":
        if request.POST.get("action") == "add":
            newWatch = Watch()
            newWatch.listing.id = listing_id
            newWatch.user.id = request.POST.get("user")
            newWatch.save()
        elif request.POST.get("action") == "remove":
            listing = Listing.objects.get(pk=3)
        else:
            listing = Listing.objects.get(pk=2)
    else:
        listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    comments = Comment.objects.all().filter(listing=listing_id)
    watches = Watch.objects.filter(listing=listing_id).count()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "watches": watches
    })
