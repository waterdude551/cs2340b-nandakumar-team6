from django.shortcuts import render
from .models import JobPost
from django.contrib.auth.decorators import login_required
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
    #need to get all job postings
    #then display them
    search_term = request.GET.get('search')
    if search_term:
        allPosts = JobPost.objects.filter(title__icontains=search_term)
    else:
        allPosts = JobPost.objects.all()
    template_data = {}
    return render(request, 'jobposting/browsing.html') #TODO

#shows one job post in detail
def viewpost(request, id):
    search_term = request.GET.get('search')
    jobpost = JobPost.objects.get(id=id)
    #get job details here
    return render(request, 'jobposting/browsepost.html') #TODO

#should have an @is recruiter or smth
@login_required
def addpost(request):
    #if request is valid
    return render(request, 'jobposting/addpost.html') #TODO