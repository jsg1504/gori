#-*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nick_name = models.TextField(max_length=36, default='')
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/%d', null=True, blank=True)
    is_expert = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(null=True, max_digits=11, decimal_places=6)
    longitude = models.DecimalField(null=True, max_digits=11, decimal_places=6)
    location = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_expert_active = models.BooleanField(default=True)
    email_uuid = models.TextField(max_length=36, null=True)
    job = models.TextField(max_length=36, null=True)
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

    def delete(self, *args, **kwargs):
        if self.profile_image:
            self.profile_image.delete()
        super(UserProfile, self).delete(*args, **kwargs)

    def add_relationship(self, user):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self,
            to_user=user)
        return relationship

    def remove_relationship(self, user):
        Relationship.objects.filter(
            from_user=self,
            to_user=user).delete()
        return

    def get_relationships(self):
        return self.relationships.filter(
            to_user__from_user=self)

    def get_related_to(self):
        return self.related_to.filter(
            from_user__to_user=self)

    def get_following(self):
        return self.get_relationships()

    def get_followers(self):
        return self.get_related_to()

    def get_friends(self):
        return self.relationships.filter(
            to_user__from_user=self,
            from_user__to_user=self)


class Relationship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='from_user')
    to_user = models.ForeignKey(UserProfile, related_name='to_user')

