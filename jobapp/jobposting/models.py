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
    
    #LOCATION DATA
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)  # can be optional if country has no states
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    #text ver of location!!
    location = models.CharField(max_length=255, blank=True)
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

    def save(self, *args, **kwargs):
        # Only process location for non-remote jobs
        if self.remote_type != 'remote':
            if self.city and self.country:
                # Build location string
                location_parts = [self.city]
                if self.state:
                    location_parts.append(self.state)
                location_parts.append(self.country)
                self.location = ', '.join(location_parts)
                
                # Geocode if coordinates not set or location changed
                if not self.latitude or not self.longitude:
                    from .utils import geocode_location
                    self.latitude, self.longitude = geocode_location(self.location)
        else:
            # Remote job - clear all location data
            self.city = ''
            self.state = ''
            self.country = ''
            self.location = ''
            self.latitude = None
            self.longitude = None
        
        super().save(*args, **kwargs)
    

    # object names in admin
    def __str__(self):
        str = "{recruiter} - {title} - ({id})"
        return str.format(recruiter = self.recruiter,
                        title=self.title,
                        id=self.id)

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