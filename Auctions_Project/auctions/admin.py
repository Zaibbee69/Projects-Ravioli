from django.contrib import admin
from .models import AuctionListing, Bid, Comment, Watchlist, User

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(User)
