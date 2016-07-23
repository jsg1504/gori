from django.db import models
from content.models import Content
from user_profile.models import UserProfile
# Create your models here.


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comment_content')
    user_profile = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comment_user_profile')
    write = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
