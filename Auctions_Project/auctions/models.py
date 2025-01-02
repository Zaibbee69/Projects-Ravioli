from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass




# Auctions listings models for handling items data
class AuctionListing(models.Model):
    CATEGORY_CHOICES = [
        ("FD", "Foods"),
        ("ET", "Entertainment"),
        ("LS", "LifeStyle"),
        ("CL", "Clothing"),
        ("HL", "Halal Category"),
        ("DL", "Daily Essentials"),
        ("TD", "Trendings"),
        ("TE", "Techno")
    ]

    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_creator")
    time = models.DateTimeField(auto_now_add=True)
    pic = models.ImageField(upload_to="auctionPics/", blank=True, null=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    auction_active = models.BooleanField(default=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def total_bids(self):
        return self.bids.count() # type: ignore

    # Showing what will be displayed when user access data
    def __str__(self) -> str:
        return f"Auction Id: {self.id} :: Name: {self.name} :: Price: {self.price} :: Date: {self.time}" # type: ignore
    

    

# Bidding model which handles all the bids made on auction listing
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

    # Showing what will be displated when user places and accesses a bid
    def __str__(self) -> str:
        return f"Bid Id: {self.id} :: Name: {self.auction} :: Price: {self.bid}" # type: ignore
    



# Comments Model for handling all the data users made on comments
class Comment(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_name")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_name")
    content = models.TextField()
    
    # Showing my commenter name
    def __str__(self) -> str:
        return f"Commentor Id: {self.id} :: Name: {self.commenter} :: Auction: {self.auction}" # type: ignore




# Watchlist model for handling if a user has put certain auctions on saving
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_auction")

    # Showing the watchlists
    def __str__(self) -> str:
        return f"User: {self.user} Auction: {self.auction}"
    



