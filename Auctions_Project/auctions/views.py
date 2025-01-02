from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import AuctionListingForm, BidForm, CommentForm
from .models import User, AuctionListing, Bid, Comment, Watchlist


def index(request):

    # Getting all the data from the database model
    listings = AuctionListing.objects.all()

    # Returning the data to the template
    return render(request, "auctions/index.html", {
        "listings": listings
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


# Function when someone wanna create something
@login_required(login_url="login")
def create(request):

    # Checking if user submitted form AKA POST
    if request.method == "POST":

        form = AuctionListingForm(request.POST, request.FILES)

        # Checking if data is valid
        if form.is_valid():

            # Not commiting to the database yet for manipulation
            auction_listings = form.save(commit=False)

            # Adding the current user to the data set
            auction_listings.creator = request.user

            # Now saving the data
            auction_listings.save()

            # redirect user to default page
            return redirect("index")
        
    # If user got here through GET   
    else: 
        form = AuctionListingForm()

    return render(request, "auctions/create.html", {
        "form": form
    })


# Function when someone accesses a certain listing by clicking it
@login_required(login_url="login")
def listing(request, listingID):

    # First getting the data and forms ready
    current_listing = get_object_or_404(AuctionListing, pk = listingID) 
    bid_form = BidForm()
    comment_form = CommentForm()
    total_bids = current_listing.total_bids()
    is_creator = False
    is_in_watchlist = False

    # Checking the current user is the creator
    if request.user == current_listing.creator:
        is_creator = True

    # Checking if the bid exists in the watchlist
    if Watchlist.objects.filter(user = request.user, auction = current_listing).exists():
        is_in_watchlist = True

    # Setting the highest bidder as none
    highest_bidder = None

    # Checking if the listings has a highest bidding
    if current_listing.highest_bid:
        highest_bid = Bid.objects.get(bid = current_listing.highest_bid, auction = current_listing)
        highest_bidder = highest_bid.bidder

    # If user submitted any kind of form then
    if request.method == "POST":

        # Checking if the user submitted someone kind of bid
        if "bid" in request.POST:

            # Getting all the data from post
            bid_form = BidForm(request.POST)

            # Checking if data is valid
            if bid_form.is_valid():

                # Temporarily saving the bid
                new_bid = bid_form.save(commit = False)

                # Now making checks if bid meets requirements
                if new_bid.bid > current_listing.price and (current_listing.highest_bid is None or new_bid.bid > current_listing.highest_bid):
                    
                    # Setting the new parameters of new bid
                    new_bid.bidder = request.user
                    new_bid.auction = current_listing
                    new_bid.save()

                    # Now setting the highest bid
                    current_listing.highest_bid = new_bid.bid
                    current_listing.save()

                    if current_listing.highest_bid:
                        highest_bid = Bid.objects.get(bid = current_listing.highest_bid, auction = current_listing)
                        highest_bidder = highest_bid.bidder

                    total_bids = current_listing.total_bids()


                    # Rendering appropriate data
                    return render(request, "auctions/listing.html", {
                        "listing": current_listing,
                        "bid_form": bid_form,
                        "comment_form": comment_form,
                        "error_message": "Bid made successfully!",
                        "is_creator": is_creator,
                        "is_in_watchlist": is_in_watchlist,
                        "highest_bidder": highest_bidder,
                        "total_bids": total_bids
                    })

                # Now setting standard if the user couldnt place high bid
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": current_listing,
                        "bid_form": bid_form,
                        "comment_form": comment_form,
                        "error_message": "Bid must be higher than the current price and the highest bid",
                        "is_creator": is_creator,
                        "is_in_watchlist": is_in_watchlist,
                        "highest_bidder": highest_bidder,
                        "total_bids": total_bids
                    })
        
        # Now checking if the user submitted some kind of comment
        if "content" in request.POST:

            # Getting all the data from the post
            comment_form = CommentForm(request.POST)

            # Checking if the data was valid
            if comment_form.is_valid():

                # Temporarily saving the new comment
                new_comment = comment_form.save(commit=False)

                # Now adding required dependencies the new comment
                new_comment.commenter = request.user
                new_comment.auction = current_listing

                # Saving the data
                new_comment.save()

                return render(request, "auctions/listing.html", {
                            "listing": current_listing,
                            "bid_form": bid_form,
                            "comment_form": comment_form,
                            "error_message": "Commented Successfully",
                            "is_creator": is_creator,
                            "is_in_watchlist": is_in_watchlist,
                            "highest_bidder": highest_bidder,
                            "total_bids": total_bids
                })
    
    # If user got here through GET method

    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "is_creator": is_creator,
        "is_in_watchlist": is_in_watchlist,
        "highest_bidder": highest_bidder,
        "total_bids": total_bids
    }) 


@login_required(login_url="login")
def add_watchlist(request, listingID):
    req_listing = get_object_or_404(AuctionListing, pk=listingID)
    Watchlist.objects.create(user= request.user, auction= req_listing)
    return redirect("listing", listingID = req_listing.id ) # type: ignore


@login_required(login_url="login")
def remove_watchlist(request, listingID):
    req_listing = get_object_or_404(AuctionListing, pk=listingID)
    Watchlist.objects.filter(user= request.user, auction= req_listing).delete()
    return redirect("listing", listingID = req_listing.id) # type: ignore


@login_required(login_url="login")
def close_listing(request, listingID):
    req_listing = get_object_or_404(AuctionListing, pk=listingID)
    if request.user == req_listing.creator:
        req_listing.auction_active = False
        req_listing.save()
    return redirect("listing", listingID = req_listing.id) #type: ignore


@login_required(login_url="login")
def watch(request):

    # First getting all the required data loaded
    watchlist = Watchlist.objects.filter(user = request.user)
    
    # if user visited the website normally
    return render(request, "auctions/watch.html", {
        "watchlist": watchlist
    })


@login_required(login_url="login")
def category(request):

    # First getting all the required data to be loaded
    auto_form = AuctionListingForm()
    results = []

    # If user submitted my form
    if request.method == "POST":

        # Temporarily saving the data first
        selected_category = request.POST.get("category")

        # Getting the data first
        results = AuctionListing.objects.filter(category = selected_category)

        # Returning the new data
        return render(request, "auctions/category.html", {
            "auto_form": auto_form,
            "results": results
        })


    # if the user visited the website normally
    return render(request, "auctions/category.html", {
        "auto_form": auto_form
    })