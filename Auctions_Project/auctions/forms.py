from django import forms
from .models import AuctionListing, Bid, Comment


# Models form for my auction lisings
class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["name", "price", "category", "description", "pic"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-light", "label": "Auction Name"}),
            "price": forms.NumberInput(attrs={"class": "form-medium"}),
            "category": forms.Select(attrs={"class": "form-dark"}),
            "description": forms.Textarea(attrs={"class": "form-text-area", "rows": 4, "columns": 40}),
            "pic": forms.ClearableFileInput(attrs={"class": "form-pic"}),
        }




# Models form my auction biddings
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]
        widgets = {
            "bid": forms.NumberInput(attrs={"class": "listing-content-main", "id": "bidCommentForm", "placeholder": "What's Your Limit!"})
        }




# Models form for my comments on auctions
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "listing-content-main", "id": "bidCommentForm"})
        }
