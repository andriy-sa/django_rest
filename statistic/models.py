from django.db import models
from users.models import User


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistic')

    type = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
