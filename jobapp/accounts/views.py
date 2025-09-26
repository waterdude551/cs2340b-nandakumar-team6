
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomErrorList
from .models import User, SeekerProfile


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')


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
            return redirect(''


def signup(request):
    template_data = {'title': 'Sign Up'}
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
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