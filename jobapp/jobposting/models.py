from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
"""
a jobpost should have:
    - id
    - job title
    - job description
    - mandatory qualifications
"""
class JobPost(models.Model):
    id = models.AutoField(primary_key=True) #<- means it should increment automatically and i dont have to care abt it
    title = models.CharField(max_length=255)
    description = models.TextField()
    qualifications = models.TextField()
    
    skills = models.TextField(default="None", blank=True, help_text="Comma-separated list of required skills")
    # LOCATION
    location = models.CharField(default="ATL, GA, US", max_length=100, help_text="City, State, Country")
    
    # SALARY RANGE - separate fields for min/max gives more flexibility
    salary_min = models.DecimalField(default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(default=1, max_digits=10, decimal_places=2, null=True, blank=True)
    
    # VISA SPONSORSHIP - Boolean field
    visa_sponsorship = models.BooleanField(default=False)
    
    def display_salary(self):
        if self.salary_min and self.salary_max:
            return f" {self.salary_min:,.0f} - {self.salary_max:,.0f}"
        elif self.salary_min:
            return f"From ${self.salary_min:,.0f}"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f}"
        return "Salary not specified"