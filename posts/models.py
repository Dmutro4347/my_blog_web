from django.contrib.auth.models import User
from django.db import models
from django.utils.text import Truncator
from autoslug import AutoSlugField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)

    def __str__(self):
        return self.title

    @property
    def description(self):
        return Truncator(self.content).chars(50, truncate="...")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)