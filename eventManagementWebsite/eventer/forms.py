from django import forms

from .models import Event, Registration, Comment, Contact


# Form for simplifying the category process
class EventFilterForm(forms.Form):
    category = forms.ChoiceField(choices=Event.CATEGORY_CHOICES, required=False, label="Filter by Category")
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "filter-form"}), required=False, label="Start Date")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class": "filter-form"}), required=False, label="End Date")


# Form for submitting the tickets process
class TicketSubmissionForm(forms.Form):
    tickets_quantity = forms.IntegerField(min_value=1, label="Ticket Quantity", widget=forms.NumberInput(attrs={"class": "ticket-form"}))


# Form for registrating straight to the data base
class RegistrationForm(forms.ModelForm):
    ticket_quantity = forms.IntegerField(min_value=1, max_value=10, label="Ticket Quantity")

    # Giving it class meta for easeabillity
    class Meta:
        model = Registration
        fields = ["event", "name", "email", "phone_number", "ticket_quantity"]
        widgets = {
            "event": forms.Select(attrs={"class": "form-event"}),
            "name": forms.TextInput(attrs={"class": "form-name"}),
            "email": forms.EmailInput(attrs={"class": "form-email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-phone"}),
            "ticket_quantity": forms.TextInput(attrs={"class": "form-ticket"}),
        }


# Form for user to make comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-comment", "placeholder": "Write your comment..."}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }