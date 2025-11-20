from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from jobposting.models import JobPost, JobApplication
import json

def show(request):
    job_posts = JobPost.objects.exclude(
        latitude__isnull=True
    ).exclude(
        longitude__isnull=True
    )
    
    jobs_data = []
    for job in job_posts:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'latitude': job.latitude,
            'longitude': job.longitude,
            'salary': job.salary,
            'remote_type': job.get_remote_type_display(),
            'skills': job.skills,
        })
    
    return render(request, 'map/map.html', {'jobs_json': json.dumps(jobs_data)})

@login_required
def applicant_map(request):
    if request.user.role != 'recruiter':
        return HttpResponseForbidden("Only recruiters can view the applicant map.")

    my_jobs = JobPost.objects.filter(recruiter=request.user)
    
    applications = JobApplication.objects.filter(
        job_post__in=my_jobs,
        seeker__seeker_profile__latitude__isnull=False,
        seeker__seeker_profile__longitude__isnull=False
    ).select_related('seeker', 'seeker__seeker_profile', 'job_post')

    applicants_data = {}

    for app in applications:
        seeker_id = app.seeker.id
        if seeker_id not in applicants_data:
            applicants_data[seeker_id] = {
                'name': f"{app.seeker.first_name} {app.seeker.last_name} ({app.seeker.username})",
                'location': app.seeker.seeker_profile.location,
                'lat': app.seeker.seeker_profile.latitude,
                'lon': app.seeker.seeker_profile.longitude,
                'applied_jobs': []
            }
        
        applicants_data[seeker_id]['applied_jobs'].append({
            'title': app.job_post.title,
            'stage': app.get_stage_display()
        })

    map_data = list(applicants_data.values())

    return render(request, 'map/applicant_map.html', {'applicants_json': json.dumps(map_data)})