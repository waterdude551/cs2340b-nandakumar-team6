# accounts/admin.py

import csv
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import UserCreationForm, UserChangeForm
from .models import User, SeekerProfile


def export_users_for_analysis(modeladmin, request, queryset):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="user_analysis_{current_time}.csv"'

    writer = csv.writer(response)

    header = [
        'User ID', 'Username', 'Role', 'Email', 'First Name', 'Last Name', 
        'Date Joined', 'Headline', 'Skills', 'Education', 'Work Experience', 
        'Links', 'Profile Email'
    ]
    writer.writerow(header)

    queryset = queryset.prefetch_related('seeker_profile')

    for user in queryset:
        seeker_profile = None
        
        try:
            seeker_profile = user.seeker_profile
        except ObjectDoesNotExist:
            seeker_profile = None

        if seeker_profile:
            seeker_data = [
                seeker_profile.headline,
                seeker_profile.skills,
                seeker_profile.education,
                seeker_profile.work_experience,
                seeker_profile.links,
                seeker_profile.email 
            ]
        else:
            seeker_data = [''] * 6 

        row = [
            user.id,
            user.username,
            user.get_role_display(),
            user.email,
            user.first_name,
            user.last_name,
            user.date_joined.isoformat() if user.date_joined else '',
        ] + seeker_data
        
        writer.writerow(row)

    return response

export_users_for_analysis.short_description = "Export selected users for stakeholder analysis (CSV)"


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
        "role",
    ]
    
    actions = [export_users_for_analysis]



admin.site.register(User, CustomUserAdmin) 

admin.site.register(SeekerProfile)