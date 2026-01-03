from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    applicants = models.IntegerField(default=0)

    def __str__(self):
        return self.title