from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:40]
    
class Post(models.Model):
    APPROVED_STATUSES = [
        ('waiting','Waiting'),
        ('approved','Approved'),
        ('declined','Declined'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    approved = models.CharField(choices=APPROVED_STATUSES, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'pk': self.id})