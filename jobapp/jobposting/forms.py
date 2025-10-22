from django import forms
from .models import JobPost, JobApplication

# Form for creating a job post based on add_post.html fields
class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title', 'skills', 'remote_type', 'city', 'state', 'country',
            'salary', 'visa_sponsorship', 'description', 'qualifications'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter job title', 'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Enter required skills', 'class': 'form-control'}),
            'remote_type': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City (e.g., Atlanta)', 'class': 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State/Province (optional)', 'class': 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country (e.g., USA)', 'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'placeholder': 'Enter salary (optional)', 'class': 'form-control'}),
            'visa_sponsorship': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter job description', 'class': 'form-control', 'rows': 4}),
            'qualifications': forms.Textarea(attrs={'placeholder': 'Enter qualifications', 'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make location fields not required by default
        self.fields['city'].required = False
        self.fields['state'].required = False
        self.fields['country'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        remote_type = cleaned_data.get('remote_type')
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')
        
        # Require location for on-site and hybrid jobs
        if remote_type in ['on-site', 'hybrid']:
            if not city:
                self.add_error('city', 'City is required for on-site and hybrid positions')
            if not country:
                self.add_error('country', 'Country is required for on-site and hybrid positions')
        return cleaned_data

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'placeholder': 'Enter a note for your application (optional)', 'class': 'form-control', 'rows': 3}),
        }