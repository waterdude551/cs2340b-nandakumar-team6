from django import forms
from accounts.models import User

class StartConversationForm(forms.Form):
    seeker = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Choose a seeker...",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your first message...',
            'rows': 5
        })
    )
    
    def __init__(self, *args, **kwargs):
        recruiter = kwargs.pop('recruiter', None)
        super().__init__(*args, **kwargs)
        
        if recruiter:
            from .models import Conversation
            # Get seekers this recruiter hasn't messaged yet
            existing_seeker_ids = Conversation.objects.filter(
                recruiter=recruiter
            ).values_list('seeker_id', flat=True)
            
            self.fields['seeker'].queryset = User.objects.filter(
                role='seeker'
            ).exclude(id__in=existing_seeker_ids)