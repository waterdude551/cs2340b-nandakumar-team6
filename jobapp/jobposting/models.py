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
    id = models.AutoField(primary_key=True) #<- means it should increment automatically and i dont have to care abt it
    title = models.CharField(max_length=255)
    description = models.TextField()
    qualifications = models.TextField()
