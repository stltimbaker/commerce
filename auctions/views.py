from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import modelform_factory

from .models import User, Category, Listing, Bid, Comment, Watch
from .forms import ListingForm

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

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watch.objects.filter(user=request.user)
    })

@login_required
def addcomment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    myComment = Comment()
    myComment.comment = request.POST.get("comment")
    myComment.listing = listing
    myComment.user = request.user
    myComment.save()

    watches = Watch.objects.filter(listing=listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    comments = Comment.objects.all().filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "watches": watches,
    })

@login_required
def addbid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    myBid = Bid()
    myBid.amount = request.POST.get("amount")
    myBid.listing = listing
    myBid.user = request.user
    myBid.save()
 
    watches = Watch.objects.filter(listing=listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    comments = Comment.objects.all().filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "watches": watches,
    })

@login_required
def openclose(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    opencloseMessage = ""
    if request.user == listing.listedBy:
        if request.POST.get("isopen") == "close":            
            listing.isOpen = False
            listing.save()
        elif request.POST.get("isopen") == "open":            
            listing.isOpen = True
            listing.save()
    else:
        opencloseMessage = "Users may only close their own listings"
    watches = Watch.objects.filter(listing=listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    comments = Comment.objects.all().filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "watches": watches,
        "opencloseMessage": opencloseMessage,
    })

@login_required
def togglewatch(request, listing_id):
    if request.POST.get("action") == "add":
        watches = 1
        addWatch = Watch()
        user = request.user
        addWatch.user = user
        listing = Listing.objects.get(pk=listing_id)
        addWatch.listing = listing
        addWatch.save()
    elif request.POST.get("action") == "remove":
        watches = 0
        removeWatch = Watch.objects.filter(listing=listing_id).filter(user=request.user)
        removeWatch.delete()
    watches = Watch.objects.filter(listing=listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    comments = Comment.objects.all().filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "watches": watches,
    })

def listing(request, listing_id):
    watches = Watch.objects.filter(listing=listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.all().filter(listing=listing_id)
    currentBid = Bid.objects.all().filter(listing=listing_id).last()
    if currentBid != None:
        currentBid = float(currentBid.amount) + .01
    comments = Comment.objects.all().filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "currentBid": currentBid,
        "comments": comments,
        "watches": watches,
    })

@login_required
def addlisting(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        form = form.save(commit=False)
        form.listedBy = request.user
        form.save()
        newForm = ListingForm()
        return render(request, "auctions/addlisting.html", {
        "form": newForm,
        "message": "Auction listing successfully added!"
        }) 
    else:
        form = ListingForm()
    return render(request, "auctions/addlisting.html", {
    "form": form
    })

def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id),
        "things": Listing.objects.all().filter(category=category_id)
    })
