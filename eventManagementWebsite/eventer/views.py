from django.shortcuts import render, redirect, get_object_or_404

# Importing utilities
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Importing my models and forms
from .models import Event, NewsLetter, Ticket, Gallery, Blog, Comment, ContactInfo, User
from .forms import EventFilterForm, TicketSubmissionForm, RegistrationForm, CommentForm, ContactForm

# Importing helper functions
from .utils import paginator_six_thousand, truncator_six_thousand




def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "eventer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "eventer/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure passwords match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eventer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "eventer/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "eventer/register.html")


# The default homepage function of the app
def index(request):

    # Finding all the featured events
    featured_events = Event.objects.filter(is_featured=True)

    # Getting all the upcoming events
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')

    # Truncate its description
    processed_featured_events = truncator_six_thousand(featured_events)

    # Getting the current page of the posts
    page_number = request.GET.get("page")

    # Calling the paginator function on it
    paginated_events = paginator_six_thousand(upcoming_events, page_number)

    # Returning all the data back to app too
    return render(request, "eventer/index.html", {
        "featured_events": processed_featured_events,
        "upcoming_events": paginated_events
    })


# When user sign up to a newsletter
def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = ""

        if NewsLetter.objects.filter(email=email).exists():
            message = render_to_string('eventer/message_template.html', {
                'message': "You're already signed to our newsletter!",
                'tags': 'error'
            })
        else:
            NewsLetter.objects.create(email=email)
            message = render_to_string('eventer/message_template.html', {
                'message': "Thank you for subscribing to our newsletter!",
                'tags': 'success'
            })

        return JsonResponse({'message': message})
    return redirect('index')

# View for users when they click on the events page
def events(request):
    
    # Setting up the form
    event_form = EventFilterForm(request.GET or None)

    # First getting all the events from the data  base
    events = Event.objects.all()

    # Checking if form data is valid
    if event_form.is_valid():
        category = event_form.cleaned_data.get("category")
        start_date = event_form.cleaned_data.get("start_date")
        end_date = event_form.cleaned_data.get("end_date")

        # Selecting the category
        if category:
            events = events.filter(category=category)

        # Checking list is upto date
        if start_date and end_date:
            events = events.filter(date__range=[start_date, end_date])

    # Now rendering the template
    return render(request, "eventer/events.html", {
        "events": events,
        "form": event_form
    })


# API to fetch data from database and give it back as JSON response
def events_feed(request):

    # Fetching all data from the data base
    events = Event.objects.all()

    # Creating an empty list to use as a JSON object
    events_list = []

    # Now looping over data and mapping it to list
    for event in events:
        events_list.append({
            "title": event.title,
            "start": event.date.isoformat(),
            "description": event.description,
            "location": event.location,
        })

    # Now returning the data
    return JsonResponse(events_list, safe=False)


# View for when user want to access a particular event details
@login_required
def event_details(request, event_id):
    
    # First getting the event that was selected
    event = get_object_or_404(Event, id=event_id)

    # Checking if the form method was POST
    if request.method == "POST":
        
        # First getting the data of the ticket
        form = TicketSubmissionForm(request.POST)

        # Checking if the data is valid
        if form.is_valid():
            
            # Getting the amount of tickets
            tickets_quantity = form.cleaned_data["tickets_quantity"]

            # Checking if their are enough available
            if event.total_tickets >= tickets_quantity:

                # Reducing inventory
                event.total_tickets -= tickets_quantity
                event.save()

                # Creating database for the user
                ticket = Ticket.objects.create(event=event, user=request.user, quantity=tickets_quantity)

                # Redirect to success page
                return redirect("index")
            
            else:
                form.add_error("tickets_quantity", "Not enough tickets available")
    
    # If request method was GET
    else:
        # Making the form standard
        form = TicketSubmissionForm()

        # Now rendering the event
        return render(request, "eventer/event_details.html", {
            "event": event,
            "form": form
        })
        # Now rendering the event
    return render(request, "eventer/event_details.html", {
        "event": event,
        "form": form
    })


# View for someone wants to register for an event
@login_required
def register_for_event(request):
    
    # If user submitted a form
    if request.method == "POST":
        # Getting the form data
        form = RegistrationForm(request.POST)

        # If the data is valid
        if form.is_valid():
            # Saving an entity of the form
            registration = form.save(commit=False)

            # Linking the user to the current logged in user
            registration.user = request.user

            registration.quantity = form.cleaned_data["ticket_quantity"]

            # Getting event data and ticket
            event = registration.event
            quantity = registration.quantity

            # Check if there are enough seats available
            if event.is_ticket_available(quantity):
                # Deducting tickets from the base
                event.tickets_sold += quantity

                # Saving stuff
                event.save()
                registration.save()

                # Now setting up data for a confirmation mail
                subject = f"Registration Confirmation for {event.title}"
                message = render_to_string("eventer/emails/confirmation_email.txt", {
                    "user": registration.user,
                    "event": event,
                    "quantity": quantity
                })

                # Sending the actual mail to the user
                send_mail(
                    subject,
                    message,
                    "zabiijaz1@gmail.com",
                    [registration.user.email],
                    fail_silently=False
                )

                # Now sending a successful message to the user
                messages.success(request, "Registration Successful! Please proceed to payment.")
                return redirect("register_for_event")
            else:
                # If quantity doesn't match
                messages.error(request, "Not enough tickets available.")
        else:
            print(form.errors)
            # Form is invalid
            messages.error(request, "Invalid form submission.")

        # If something went wrong, redirect back to the form
        return redirect("register_for_event")
    
    # If GET request, render the empty form
    else: 
        # Setting up the form
        form = RegistrationForm()

        # Now rendering data
        return render(request, "eventer/register_event.html", {
            "form": form,
        })


# View for when a user wants to visit the gallery page
def gallery(request):

    # Getting all the images from the database
    images = Gallery.objects.all()

    # Rendering the data
    return render(request, "eventer/gallery.html", {
        "images": images
    })


# View for displaying all the blogs
def blog(request):

    # Getting all the blog posts
    posts = Blog.objects.all().order_by("-created_at")

    # Rendering said data
    return render(request, "eventer/blogs.html", {
        "posts": posts
    })


# View for each individual blog post
def blog_detail(request, blog_id):

    # Getting the said blog
    post = get_object_or_404(Blog, id=blog_id)

    # Getting all the comments made on this post
    comments = post.comments.all().order_by("-created_at")

    # If user made a comment then
    if request.method == "POST":

        # Getting data from form
        form = CommentForm(request.POST)

        # Checking that data is valid
        if form.is_valid():

            # Saving an instance of the comment
            comment = form.save(commit=False)

            # Setting up the fields for data
            comment.post = post
            comment.author = request.user

            # Saving and redirecting to template
            comment.save()
            return redirect("blog_detail", blog_id=blog_id)
        
    # Other wise if GET was used
    else:

        # Setting up the comment form
        form = CommentForm()

        # Rendering said post
        return render(request, "eventer/blog_details.html", {
            "post": post,
            "comments": comments,
            "form": form
        })
    

def contact_page(request):
    contact_info = ContactInfo.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            # Send email notification
            send_mail(
                subject='New Contact Form Submission',
                message=f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\nPhone: {form.cleaned_data['phone_number']}\nMessage: {form.cleaned_data['message']}",
                from_email='youremail@example.com',
                recipient_list=['yourbusiness@example.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_page')
        else:
            messages.error(request, 'There was an error in your form submission. Please try again.')
    
    else:
        form = ContactForm()

    return render(request, 'eventer/contact.html', {
        "form": form,
        'contact_info': contact_info
    })