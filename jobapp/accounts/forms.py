from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import User, SeekerProfile

from django.forms.utils import ErrorList

from django.utils.safestring import mark_safe

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class CustomErrorList(ErrorList):

    def __str__(self):

        if not self:

            return ''

        return mark_safe(''.join([ f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "role")

    def __init__(self, *args, **kwargs):

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:

            self.fields[fieldname].help_text = None

            self.fields[fieldname].widget.attrs.update(

                {'class': 'form-control'}

            )

        # Hide 'admin' from role choices if role field exists
        if 'role' in self.fields:
            choices = self.fields['role'].choices
            self.fields['role'].choices = [c for c in choices if c[0] != 'admin']

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username",)

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['headline', 'skills', 'education', 'work_experience', 'links', 'email']

    def clean_links(self):
        links = self.cleaned_data['links']
        url_validator = URLValidator()
        for link in [l.strip() for l in links.split(',') if l.strip()]:
            try:
                url_validator(link)
            except ValidationError:
                raise ValidationError(f"'{link}' is not a valid URL.")
        return links

class EmailSeekerForm(forms.Form):
    # The seeker's email — displayed but not editable
    to_email = forms.EmailField(
        label="To",
        disabled=True,
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
        })
    )

    # Subject line for the message
    subject = forms.CharField(
        label="Subject",
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter subject"
        })
    )

    # Email body
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 6,
            "placeholder": "Write your message here..."
        })
    )