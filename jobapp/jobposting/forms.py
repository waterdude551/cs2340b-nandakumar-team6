from django import forms
from .models import JobPost, JobApplication

# Form for creating a job post based on add_post.html fields
class JobPostForm(forms.ModelForm):
	class Meta:
		model = JobPost
		fields = [
			'title', 'skills', 'location', 'salary', 'remote_type', 'visa_sponsorship', 'description', 'qualifications'
		]
		widgets = {
			'title': forms.TextInput(attrs={'placeholder': 'Enter job title here', 'class': 'form-control'}),
			'skills': forms.TextInput(attrs={'placeholder': 'Enter required skills', 'class': 'form-control'}),
			'location': forms.TextInput(attrs={'placeholder': 'Enter job location', 'class': 'form-control'}),
			'salary': forms.TextInput(attrs={'placeholder': 'Enter salary (optional)', 'class': 'form-control'}),
			'remote_type': forms.Select(attrs={'class': 'form-control'}),
			'visa_sponsorship': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'description': forms.Textarea(attrs={'placeholder': 'Enter job description here', 'class': 'form-control', 'rows': 4}),
			'qualifications': forms.Textarea(attrs={'placeholder': 'Enter mandatory qualifications here', 'class': 'form-control', 'rows': 3}),
		}

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'placeholder': 'Enter a note for your application (optional)', 'class': 'form-control', 'rows': 3}),
        }