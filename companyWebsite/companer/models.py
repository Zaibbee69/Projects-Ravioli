from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.



# Model for the user
class User(AbstractUser):
    pass

# Model for making nav bar items dynamic
class NavigationElements(models.Model):

    # Adding meta class for better sorting
    class Meta:
        ordering = ["name"]
        verbose_name = "Navigation Element"
        verbose_name_plural = "Navigation Elements"

    # Defining the entities of the model
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=255)
    is_dropdown = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    # Defining the model
    def __str__(self) -> str:
        return self.name


# Model for making the Banner dynamic
class BannerContent(models.Model):
    tagline = models.CharField(max_length=200)
    video = models.FileField(upload_to="banner_videos/")
    learn_more_link = models.URLField(max_length=255)
    get_started_link = models.URLField(max_length=255)

    # Defining the model
    def __str__(self) -> str:
        return self.tagline

class CompanyOverview(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    

# Model for company values
class CompanyValue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
# Model for displaying all the milestones
class Milestones(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='milestone_images/', blank=True, null=True)


# Model for all the services
class Service(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    icon = models.CharField(max_length=64)

    def __str__(self):
        return self.title
    

# Model for clients testimonials
class ClientTestimonial(models.Model):
    client_name = models.CharField(max_length=64)
    client_image = models.ImageField(upload_to="testimonials/")
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    video = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.client_name} - {self.rating} Stars'
    

# Model for clients videos

class VideoTestimonial(models.Model):
    client_name = models.CharField(max_length=255)
    video_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return f'{self.client_name} Video Testimonial'
    

# Model for setting categories of projects
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# Model for projects
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    case_study_link = models.URLField()
    date = models.DateField()
    client = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name


# Model to store contact info
class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.email


# Model for storing newsletter info
class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
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