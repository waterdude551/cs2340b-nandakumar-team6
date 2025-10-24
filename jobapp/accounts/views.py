
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .forms import CustomUserCreationForm, CustomErrorList, EmailSeekerForm
from .models import User, SeekerProfile, SavedFilter
from django.core.mail import send_mail
from django.contrib import messages


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


def login(request):
    template_data = {'title': 'Login'}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home')


def signup(request):
    template_data = {'title': 'Sign Up'}
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save()
            
            # Create SeekerProfile if user is a seeker
            if user.role == 'seeker':
                SeekerProfile.objects.create(user=user)
            
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})


@login_required
def profile(request, id):
    user = get_object_or_404(User, id=id)
    seeker_profile = None
    if user.role == "seeker":
        seeker_profile = getattr(user, 'seeker_profile', None)
    return render(request, 'accounts/profile.html', {'profile': user, 'seeker_profile': seeker_profile})


@login_required
@require_http_methods(["GET", "POST"])
def edit_profile(request, id):
    if request.user.id != id:
        return redirect('accounts.profile', id=request.user.id)
    user = request.user

    # If user is a seeker, get or create the SeekerProfile instance
    seeker_profile = None
    if user.role == "seeker":
        seeker_profile, created = SeekerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        # Always update seeker fields for seekers
        if seeker_profile:
            seeker_profile.headline = request.POST.get('headline', seeker_profile.headline)
            seeker_profile.skills = request.POST.get('skills', seeker_profile.skills)
            seeker_profile.education = request.POST.get('education', seeker_profile.education)
            seeker_profile.work_experience = request.POST.get('work_experience', seeker_profile.work_experience)
            seeker_profile.links = request.POST.get('links', seeker_profile.links)
            seeker_profile.save()
        return redirect('accounts.profile', id=user.id)

    # Prepare initial data for the form fields
    initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    if seeker_profile:
        initial.update({
            'headline': seeker_profile.headline,
            'skills': seeker_profile.skills,
            'education': seeker_profile.education,
            'work_experience': seeker_profile.work_experience,
            'links': seeker_profile.links,
        })
    return render(request, 'accounts/edit_profile.html', {'user': user, 'initial': initial})

def search_users(request):
    if request.method == 'POST' and request.user.is_authenticated:
        filter_name = request.POST.get('filter_name')
        filters = request.GET.dict()

        if filter_name and filters:
            SavedFilter.objects.create(user=request.user, name=filter_name, filters=filters)
        
        return redirect(request.path_info + '?' + request.GET.urlencode())

    query = request.GET.get('q', '')
    user_type = request.GET.get('user_type', 'seeker')
    skills = request.GET.get('skills', '')
    education = request.GET.get('education', '')
    work_experience = request.GET.get('work_experience', '')
    headline = request.GET.get('headline', '')
    company = request.GET.get('company', '')
    recruiter_title = request.GET.get('recruiter_title', '')
    
    users = User.objects.filter(role=user_type)
    
    from django.db.models import Q
    if query:
        name_parts = query.strip().split()
        q_obj = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        if len(name_parts) >= 2:
            first, last = name_parts[0], name_parts[-1]
            q_obj = q_obj | (Q(first_name__icontains=first) & Q(last_name__icontains=last))
        users = users.filter(q_obj)

    if user_type == 'seeker':
        if skills:
            users = users.filter(seeker_profile__skills__icontains=skills)
        if education:
            users = users.filter(seeker_profile__education__icontains=education)
        if work_experience:
            users = users.filter(seeker_profile__work_experience__icontains=work_experience)
        if headline:
            users = users.filter(seeker_profile__headline__icontains=headline)
    
    if user_type == 'recruiter':
        if company:
            users = users.filter(first_name__icontains=company)
        if recruiter_title:
            users = users.filter(last_name__icontains=recruiter_title)

    saved_filters = []
    if request.user.is_authenticated:
        saved_filters = SavedFilter.objects.filter(user=request.user)

    context = {
        'users': users,
        'query': query,
        'skills': skills,
        'education': education,
        'work_experience': work_experience,
        'headline': headline,
        'company': company,
        'recruiter_title': recruiter_title,
        'user_type': user_type,
        'saved_filters': saved_filters,
    }

    return render(request, 'accounts/search.html', context)

def email_seeker(request, id):
    recruiter = request.user
    seeker = get_object_or_404(User, id=id)
    form = EmailSeekerForm(initial={'to_email': seeker.email})
    return render(request, 'accounts/email_seeker.html', {'recruiter': recruiter, 'seeker': seeker, 'form': form})

def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = f"Recruiter {request.user.email} sent you this message:\n\n" + request.POST.get('message', '')
        to_email = request.POST.get('to_email', '')
        #from_email = request.user.email

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
        messages.success(request, f"Email successfully sent to {to_email}!")
        return redirect('accounts.search') 
    else:
        return redirect('accounts.search')
    
@login_required
def delete_filter(request, filter_id):
    filter_to_delete = get_object_or_404(SavedFilter, id=filter_id, user=request.user)
    filter_to_delete.delete()
    return redirect('accounts.search')