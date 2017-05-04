from django.db import models
from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    description = models.TextField(default='')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
