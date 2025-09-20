from django.shortcuts import render

"""
GOALS:
    - should have a model called job post
    - should have a url that displays all job postings
    - should be able to go to an individual job
    - should have a url that displays stuff for adding a job
    - should be similar to reviews / review posting
"""

# Create your views here.
#shows all job postings
def browsing(request):
    #need to get all job postings
    #then display them
    return render(request, 'jobposting/browsing.html') #TODO

#shows one job post in detail
def browsepost(request, id):
    #get job details here
    return render(request, 'jobposting/browsepost.html') #TODO

#should have an @is recruiter or smth
def addpost(request):
    return render(request, 'jobposting/addpost.html') #TODO