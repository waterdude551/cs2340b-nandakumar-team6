from django.shortcuts import render
from jobposting.models import JobPost
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