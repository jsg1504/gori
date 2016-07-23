from django.db import models
from content.models import Content
from user_profile.models import UserProfile
# Create your models here.


class Like(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='like_content')
    user_profile = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='like_user_profile')
    created_at = models.DateTimeField(auto_now_add=True)
