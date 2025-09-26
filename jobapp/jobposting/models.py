from django.db import models
from accounts.models import User

# Create your models here.
"""
a jobpost should have:
    - id
    - job title
    - job description
    - mandatory qualifications
"""
class JobPost(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    skills = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True)
    REMOTE_CHOICES = [
        ('remote', 'Remote'),
        ('on-site', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]
    remote_type = models.CharField(max_length=10, choices=REMOTE_CHOICES, default='on-site')
    visa_sponsorship = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)
    qualifications = models.CharField(max_length=1000)

class JobApplication(models.Model):
    id = models.AutoField(primary_key=True)
    STAGE_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('offer', 'Offered'),
        ('closed', 'Closed'),
    ]
    stage = models.CharField(max_length=50, default='applied', choices=STAGE_CHOICES)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    note = models.TextField(max_length=255)
    applied_at = models.DateTimeField(auto_now_add=True)