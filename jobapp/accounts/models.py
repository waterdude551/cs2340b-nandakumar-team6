from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):
    # add additional fields in here
    ROLES = (('seeker', 'Job Seeker'), ('recruiter', 'Job Recruiter'), ('admin', "Site Administrator"))
    role = models.CharField(max_length=10, choices=ROLES)

    objects = UserManager()

    def __str__(self):
        return self.username
    
class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    headline = models.CharField(max_length=100, default="")
    skills = models.CharField(max_length=300, default="")
    education = models.CharField(max_length=200, default="")
    work_experience = models.CharField(max_length=200, default="")
    links = models.CharField(max_length=300, default="")
    email = models.CharField(max_length=300, default="")
    
    location = models.CharField(max_length=255, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    visibility_settings = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.location:
            try:
                old_profile = SeekerProfile.objects.get(pk=self.pk)
                if old_profile.location != self.location or not self.latitude:
                    do_geocode = True
                else:
                    do_geocode = False
            except SeekerProfile.DoesNotExist:
                do_geocode = True

            if do_geocode:
                from jobposting.utils import geocode_location
                self.latitude, self.longitude = geocode_location(self.location)
        else:
            self.latitude = None
            self.longitude = None
            
        super().save(*args, **kwargs)
    
class SavedFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    filters = models.JSONField()

    def __str__(self):
        return f'{self.user.username} - {self.name}'