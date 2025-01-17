from django import forms

from .models import NewPost

# Form for when user wants to create a new post
class NewPostForm(forms.ModelForm):
    class Meta:
        model = NewPost
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-text-area", "placeholder": "What's on your mind?", "rows": 4, "columns": 30}),
        }