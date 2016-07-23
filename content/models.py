from django.db import models
from user_profile.models import UserProfile


class Content(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='content/images/%Y/%m/%d', null=True)
    # TODO: add video file
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    content_type = models.IntegerField()
    state = models.IntegerField(default=1)

