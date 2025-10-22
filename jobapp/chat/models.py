from django.db import models
from accounts.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    message = models.TextField(max_length=300)