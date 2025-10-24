
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, SeekerProfile

admin.site.register(User)
admin.site.register(SeekerProfile)

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]