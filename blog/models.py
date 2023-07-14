# django models helps us in creating object relational mapping, which helps and saves us the time of writing sql codes by mapping the objects to the database

# migrations are useful because they help us to create the database tables and columns for us, instead of us writing the sql codes ourselves and also it helps to edit the database without writing complex sql codes

# how to make migrations: python manage.py makemigrations and then python manage.py migrate

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # if user is deleted, delete the post as well
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # this dunder method is used to return the title of the post when we call the post object

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
