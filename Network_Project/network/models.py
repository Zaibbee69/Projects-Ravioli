from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)


# Model For the posts the user makes
class NewPost(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator", blank=False)
    content = models.TextField(blank=False)
    time = models.DateTimeField( default=timezone.now )
    likes = models.ManyToManyField("User", related_name="liked_posts", blank=True)

    def like_count(self):
        return self.likes.count()

    # Function when user accesses this model
    def __str__(self) -> str:
        return f"Created by {self.creator} content is {self.content}"