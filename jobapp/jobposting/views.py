from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import JobPost, JobApplication
from .forms import JobPostForm, JobApplicationForm
"""
GOALS:
    - should have a model called job post (DONE)
        - has id
        - has title
        - has job description
        - has qualifications
    - should have a url that displays all job postings
        - should pass a list of all job posts (DONE)
        - should be searchable (DONE)
            - by title?
            - by job description?
            - by qualifications?
    - should be able to go to an individual job by id
        - if seeker: should be able to apply?
        - if recruiter: can edit?
    - should have a url that redirects to add job post page
        - should only appear for recruiters
        - should have a form where recruiters fill out title, desc, qualifications

    note: should be similar to reviews / review posting!!
"""

# Create your views here.
#shows all job postings
def browsing(request):
    jobposts = JobPost.objects.all()
    title = request.GET.get('title', '')
    skills = request.GET.get('skills', '')
    location = request.GET.get('location', '')
    salary = request.GET.get('salary', '')
    remote_type = request.GET.get('remote_type', '')
    visa_sponsorship = request.GET.get('visa_sponsorship', '')

    if title:
        jobposts = jobposts.filter(title__icontains=title)
    if skills:
        jobposts = jobposts.filter(skills__icontains=skills)
    if location:
        jobposts = jobposts.filter(location__icontains=location)
    if salary:
        jobposts = jobposts.filter(salary__icontains=salary)
    if remote_type:
        jobposts = jobposts.filter(remote_type=remote_type)
    if visa_sponsorship == 'true':
        jobposts = jobposts.filter(visa_sponsorship=True)
    elif visa_sponsorship == 'false':
        jobposts = jobposts.filter(visa_sponsorship=False)

    return render(request, 'jobposting/list_posts.html', {'jobposts': jobposts})

#shows one job post in detail
def viewpost(request, id):
    jobpost = JobPost.objects.get(id=id)
    can_edit = request.user.is_authenticated and jobpost.recruiter == request.user
    form = None
    if request.user.is_authenticated and getattr(request.user, "role", None) == "seeker":
        form = JobApplicationForm()
    return render(request, 'jobposting/view_post.html', {'jobpost': jobpost, 'can_edit': can_edit, 'form': form})

#should have an @is recruiter or smth
from .forms import JobPostForm

@login_required
def addpost(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            jobpost = form.save(commit=False)
            jobpost.recruiter = request.user
            jobpost.save()
            return render(request, 'jobposting/add_post.html', {'form': JobPostForm(), 'success': True})
    else:
        form = JobPostForm()
    return render(request, 'jobposting/add_post.html', {'form': form})

@login_required
def edit_post(request, id):
    jobpost = JobPost.objects.get(id=id)
    if jobpost.recruiter != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=jobpost)
        if form.is_valid():
            form.save()
            return redirect('jobposting.viewpost', id=jobpost.id)
    else:
        form = JobPostForm(instance=jobpost)
    return render(request, 'jobposting/edit_post.html', {'form': form, 'jobpost': jobpost})

from .forms import JobApplicationForm
def apply(request, id):
    jobpost = JobPost.objects.get(id=id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_post = jobpost
            application.seeker = request.user
            application.save()
            return redirect('jobposting.viewpost', id=jobpost.id)
    else:
        form = JobApplicationForm()
    return render(request, 'jobposting/apply.html', {'form': form, 'jobpost': jobpost})
@login_required
def list_applications(request, jobpost_id):
    jobpost = JobPost.objects.get(id=jobpost_id)
    sort = request.GET.get('sort', 'date')
    direction = request.GET.get('dir', 'desc')
    hide_closed = request.GET.get('hide_closed', '0') == '1'
    applications = jobpost.applications.select_related('seeker').all()
    if hide_closed:
        applications = applications.exclude(stage='closed')

    # Custom stage order for sorting
    stage_order = ['applied', 'under_review', 'interview', 'offer', 'closed']
    if sort == 'stage':
        # Annotate with custom order
        def stage_key(app):
            try:
                return stage_order.index(app.stage)
            except ValueError:
                return len(stage_order)
        applications = sorted(applications, key=stage_key, reverse=(direction=='desc'))
    else:
        if sort == 'applicant':
            order = 'seeker__username'
        else:
            order = 'applied_at'
        if direction == 'desc':
            order = '-' + order
        applications = applications.order_by(order)

    return render(request, 'jobposting/list_applications.html', {
        'applications': applications,
        'jobpost': jobpost,
        'sort': sort,
        'dir': direction,
        'hide_closed': hide_closed
    })

@login_required
def update_application_stage(request, application_id, jobpost_id):
    application = JobApplication.objects.get(id=application_id)
    jobpost = JobPost.objects.get(id=jobpost_id)
    # Only allow recruiter of the job post to update
    if jobpost.recruiter != request.user:
        return HttpResponseForbidden("You are not allowed to update this application.")
    if request.method == 'POST':
        new_stage = request.POST.get('stage')
        if new_stage in dict(JobApplication.STAGE_CHOICES):
            application.stage = new_stage
            application.save()
    return redirect('jobposting.list_applications', jobpost_id=jobpost.id)

@login_required
def seeker_applications(request):
    if getattr(request.user, "role", None) != "seeker":
        return HttpResponseForbidden("You are not authorized to view this page.")

    applications = JobApplication.objects.filter(seeker=request.user).order_by('-applied_at').select_related('job_post')

    return render(request, 'jobposting/seeker_applications.html', {'applications': applications})