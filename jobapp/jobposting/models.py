from django.db import models

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
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    qualifications = models.CharField(max_length=1000)