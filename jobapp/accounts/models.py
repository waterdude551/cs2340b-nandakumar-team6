from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # add additional fields in here
    ROLES = (('seeker', 'Job Seeker'), ('recruiter', 'Job Recruiter'))
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return self.username
    
class Seeker(User):
    headline = models.CharField(max_length=100, default="")
    skills = models.CharField(max_length=300, default="")
    education = models.CharField(max_length=200, default="")
    work_experience = models.CharField(max_length=200, default="")
    links = models.CharField(max_length=300, default="")
    pass

class Recruiter(User):
    pass