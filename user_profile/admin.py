from django.contrib import admin
from user_profile.models import UserProfile
from django.contrib.auth.models import User

admin.site.register(UserProfile)
# admin.site.register(User, UserProfile)
