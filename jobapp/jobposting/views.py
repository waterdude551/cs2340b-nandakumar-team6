from django.shortcuts import render, redirect
from .models import JobPost
from django.contrib.auth.decorators import login_required
"""
GOALS:
    - should have a model called job post 
        - has id (DONE)
        - has title (DONE)
        - has job description (DONE)
        - has qualifications (DONE)
        - SKILLS
        - LOCATION
        - SALARY RANGE
        - REMOTE/ON-SITE/HYBRID
        - VISA SPONSORSHIP
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
    #search_term = request.GET.get('search')
    #if search_term:
    #    allPosts = JobPost.objects.filter(title__icontains=search_term)
    #else:
    allPosts = JobPost.objects.all()
    print(allPosts)
    template_data = {}
    template_data['jobPosts'] = allPosts
    return render(request, 'jobposting/browsing.html', {'template_data': template_data})

#shows one job post in detail
def viewpost(request, id):
    jobpost = JobPost.objects.get(id=id)
    #get job details here
    template_data = {}
    template_data['jobPost'] = jobpost
    return render(request, 'jobposting/browsepost.html', {'template_data': template_data}) #TODO

#should have an @is recruiter or smth
#SHOULD PROBABLY CHANGE NAME TO BE CLEAR THIS IS THE PAGE
@login_required
def addpost(request):
    #if request is valid
    return render(request, 'jobposting/addpost.html') #TODO

#this is the method that makes the new job id
@login_required
def createpost(request):
    print("HIII")
    if request.method == 'POST' and request.POST['title'] != '' and request.POST['description'] != '' and request.POST['qualifications'] != '':
        post = JobPost()
        post.title = request.POST['title']
        post.description = request.POST['description']
        post.qualifications = request.POST['qualifications']
        post.user = request.user
        post.save()
        return redirect('jobposting.browsing')
    else:
        return redirect('jobposting.browsing')
    