from django.db import models
from accounts.models import User

# Create your models here.
from django.db import models
from accounts.models import User

# Create your models here.
class Conversation(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations_as_recruiter'
    )
    seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations_as_seeker'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('recruiter', 'seeker')  # Prevents duplicate conversations
        ordering = ['-updated_at']  # Newest conversations first
    
    def __str__(self):
        return f"{self.recruiter.username} → {self.seeker.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_sent'
    )
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sent_at']  # Oldest messages first (chronological order)
    
    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}"