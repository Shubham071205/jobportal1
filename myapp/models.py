from django.db import models
from django.contrib.auth.models import User


# =====================================
# JOB MODEL
# =====================================

class Job(models.Model):
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # auto maintained counter
    applicants = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =====================================
# JOB SEEKER PROFILE
# =====================================

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seeker_profile"
    )

    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# =====================================
# COMPANY PROFILE
# =====================================

class CompanyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    about_company = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username


# =====================================
# APPLICATION MODEL
# =====================================

class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    class Meta:
        unique_together = ("job", "seeker")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.seeker.username} → {self.job.title}"
