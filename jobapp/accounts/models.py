from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Seeker(User):
    headline = models.CharField(max_length=255)
    pass

class Recruiter(User):
    pass
