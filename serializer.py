from user_profile.models import UserProfile
from django.contrib.auth.models import User
from content.models import Content
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)


class UserProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    nick_name = serializers.CharField(max_length=36)
    profile_image = serializers.CharField()
    description = serializers.CharField()
    last_login = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    job = serializers.CharField()

    # content_count = serializers.IntegerField(source='content_set.count', read_only=True)

    def get_queryset(self):
        queryset = Content.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user_profile__user__username=username)
        return queryset


class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_profile = UserProfileSerializer()
    image_file = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.CharField()
    content_type = serializers.IntegerField()


class RelationshipSerializer(serializers.Serializer):
    from_user = UserProfileSerializer()
    to_user = UserProfileSerializer()


# class UserProfileDetailSerializer(serializers.Serializer):
#     user = UserSerializer()
#     nick_name = serializers.CharField(max_length=36)
#     profile_image = serializers.CharField()
#     description = serializers.CharField()
#     last_login = serializers.CharField()
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()
#     job = serializers.CharField()
#     user_content_count = serializers.IntegerField(source='content_set.count', read_only=True)
#     user_follower_count = serializers.IntegerField(source='get_related_to.count', read_only=True)
#     user_following_count = serializers.IntegerField(source='get_relationships.count', read_only=True)
