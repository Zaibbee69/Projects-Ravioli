from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Model for an user made arbitary right now
class User(AbstractUser):
    pass

# Model for each event
class Event(models.Model):

    # Choices for what different type of category events can exist
    CATEGORY_CHOICES = [
        ("Conference", "Conference"),
        ("Workshop", "Workshop"),
        ("Party", "Party"),
        ("Exhibition", "Exhibition"),
        ("Trip", "Trip"),
        ("Cozy Events", "Cozy Events"),
        ("Thrilling Events", "Thrilling Events"),
        ("Corporate Events", "Corporate Events")
    ]

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    schedule = models.CharField(max_length=100, null=True, blank=True)
    learn_more_url = models.URLField(max_length=100, blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    # Defining an event
    def __str__(self):
        return self.title

    # Method to check wether tickets are available or noe
    def is_ticket_available(self, quantity):
        return self.total_tickets - self.tickets_sold >= quantity
    
    # Sorting data by itself
    class Meta():
        ordering = ["date"]


# Model for newsletter signups
class NewsLetter(models.Model):
    email = models.EmailField(unique=True)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

# Model for tickets signups on users
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Defining naming convention
    def __str__(self):
        return self.event


# Model for registration for events
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField(default=1)
    registration_date = models.DateTimeField(auto_now_add=True)

        # Defining naming convention
    def __str__(self):
        return self.name


# Model to handle the gallery images
class Gallery(models.Model):

    MEDIA_TYPE_CHOICE = [
        ("image", "Image"),
        ("video", "Video")
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICE, default="image")
    image = models.ImageField(upload_to="gallery_images/")
    video_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Defining what the table means
    def __str__(self):
        return self.title


# Model for all the blog posts
class Blog(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Defining a blog 
    def __str__(self):
        return self.title
    

# Model for comments related to posts
class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Defining a comment
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    

# Model for Contact
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

# Company data model
class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.email
    