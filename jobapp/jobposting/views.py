from django.shortcuts import render

"""
GOALS:
    - should have a model called job post
    - should have a url that displays all job posting
    - should have a url that displays stuff for adding a job

TO DO:
    - double check 
"""

# Create your views here.
def browsing(request):
    #need to get all job postings
    #then display them
    return render(request, 'jobposting/browsing.html') #TODO

def addpost(request):
    return render(request, 'jobposting/addpost.html') #TODO