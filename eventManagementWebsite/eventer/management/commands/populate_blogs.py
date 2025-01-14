from django.core.management.base import BaseCommand
from eventer.models import Blog, User  # Import your custom User model and Blog model
import random

class Command(BaseCommand):
    help = 'Populate the database with fun blog posts for testing'

    def handle(self, *args, **kwargs):
        titles = [
            "The Secret Life of a Banana",
            "How to Survive a Zombie Apocalypse",
            "The Mysteries of Unicorns",
            "10 Hilarious Pranks to Pull on Your Friends",
            "A Guide to Building Your Own Robot",
            "Why Cats Are the Best Roommates",
            "The Ultimate Guide to DIY Ice Cream Flavors",
            "The Most Epic Dance Moves to Master"
        ]

        excerpts = [
            "Discover what your bananas do when you’re not looking.",
            "Essential tips to stay safe and have fun during a zombie apocalypse.",
            "Uncover the truth behind unicorns and their magical powers.",
            "Pull these pranks and become the office legend.",
            "Step-by-step guide to creating your very own robot companion.",
            "The reasons why cats make the ultimate roommates.",
            "Create the most unique ice cream flavors right in your kitchen.",
            "Master these dance moves and impress everyone at your next party."
        ]

        contents = [
            "Have you ever wondered what bananas do when no one is around? In this post, we explore the secret life of these yellow fruits and their hidden adventures.",
            "A zombie apocalypse might sound like a plot from a movie, but being prepared is essential. Learn how to survive, protect yourself, and thrive in this ultimate guide.",
            "Unicorns have been a part of folklore for centuries, but are they real? Find out what these magical creatures are all about and how they have inspired myths.",
            "Looking for some light-hearted fun? Try these hilarious pranks that will have everyone in stitches and make you the prankster king or queen of the office.",
            "Building a robot might seem like something from a sci-fi movie, but with our guide, you’ll be able to create a functioning robot that can assist you in daily tasks.",
            "Cats are known for their independence and quirky behaviors, but they also make wonderful companions. Discover why cats are the best roommates you could ask for.",
            "Ice cream is a treat enjoyed by many, but why not make it even better? Learn how to create exciting and unusual ice cream flavors at home with our easy recipes.",
            "Dancing is a great way to express yourself and have fun. Master these epic dance moves to show off at parties and become the center of attention."
        ]

        # Define some predefined users
        predefined_users = [
            {"username": "john_doe", "password": "password123", "email": "john@example.com"},
            {"username": "jane_smith", "password": "password123", "email": "jane@example.com"},
            {"username": "alex_jones", "password": "password123", "email": "alex@example.com"},
            {"username": "lisa_white", "password": "password123", "email": "lisa@example.com"}
        ]

        # Create predefined users if they don't exist
        for user_data in predefined_users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"]}
            )
            if created:
                user.set_password(user_data["password"])
                user.save()

        users = User.objects.all()

        for i in range(8):
            Blog.objects.create(
                title=random.choice(titles),
                excerpt=random.choice(excerpts),
                content=random.choice(contents),
                author=random.choice(users)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with blog posts'))
