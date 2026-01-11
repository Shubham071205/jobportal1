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


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    about_company = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username
