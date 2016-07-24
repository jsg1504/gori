#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import get_token
from uuid import uuid4
from decimal import Decimal
from django.core import serializers
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from serializer import UserProfileSerializer
from serializer import UserSerializer
from serializer import RelationshipSerializer
from content.models import Content
import json
import logging
from django.core.mail import EmailMessage


def profile(request, username):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
    if request.method == 'GET':
        user_profile = User.objects.get(username=username).userprofile
        serializer = UserProfileSerializer(user_profile)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


def get_profile_detail(request, username):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
    if request.method == 'GET':
        user_profile = User.objects.get(username=username).userprofile
        user_content_count = Content.objects.filter(user_profile=user_profile, is_active=True).count()
        user_follower_count = user_profile.get_followers().count()
        user_following_count = user_profile.get_following().count()
        return JsonResponse({'status': 'success', 'user_content_count': user_content_count, 'user_follower_count': user_follower_count, 'user_following_count': user_following_count})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def my_info(request):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
    if request.method == 'GET':
        user_profile = User.objects.get(username=request.user.username).userprofile
        serializer = UserProfileSerializer(user_profile)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


def mobile_login_after(request):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    return JsonResponse({'status': 'success', 'session': request.user.get_session_auth_hash()})


def token_csrf(request):
    return JsonResponse({'status': 'success', 'csrf_token': get_token(request)})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        authentication_form = AuthenticationForm
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            user_profile = request.user.userprofile
            if not user_profile.is_active:
                auth_logout(request)
                return JsonResponse({'status': 'error', 'error_code': '204', 'desc': 'email'})
            serializer = UserProfileSerializer(user_profile)
            return JsonResponse(serializer.data, safe=False)
            # return JsonResponse({'status': 'success', 'session': request.user.get_session_auth_hash()})
        else:
            return JsonResponse({'status': 'error', 'error_code': '203', 'desc': 'username password missmatch'})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        is_exist = True
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            is_exist = False
        if is_exist :
            return JsonResponse({'status': 'error', 'error_code': '200', 'desc': 'username is exist'})

        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            is_exist = False
        if is_exist:
            return JsonResponse({'status': 'error', 'error_code': '201', 'desc': 'email is exist'})

        password = request.POST['password']

        is_expert = int(request.POST['is_expert'])

        user = User.objects.create_user(username=username, password=password, email=email)
        uuid = uuid4().hex
        if is_expert == 0:
            UserProfile.objects.create(is_expert=False, user=user, email_uuid=uuid, is_active=False)
        elif is_expert == 1:
            UserProfile.objects.create(is_expert=True, user=user, email_uuid=uuid, is_active=False)
        # TODO: send email uuid url, SMTP Server
        # TODO: generate cert URL
        cert_url = settings.SERVER_URL + 'accounts/' + username + '/' + uuid + '/'
        email = EmailMessage('Email certification', cert_url, to=[email])
        email.send()
        # logger.debug('cert_url:' + cert_url)

        return JsonResponse({'status': 'success', 'username': username})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def cert_email(request, username, uuid):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.email_uuid == uuid:
            user_profile.is_active = True
            user_profile.save()
            return JsonResponse({'status': 'success', 'username': username})
        else:
            return JsonResponse({'status': 'error', 'error_code': '202', 'desc': 'uuid mismatch'})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_user_list_by_distance(request, latitude_l_t, longitude_l_t, latitude_r_b, longitude_r_b):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})

        # left top
        lat_l_t = Decimal(latitude_l_t)
        lng_l_t = Decimal(longitude_l_t)
        # right bottom
        lat_r_b = Decimal(latitude_r_b)
        lng_r_b = Decimal(longitude_r_b)

        user_profile_array = UserProfile.objects.filter(latitude__range=(lat_r_b, lat_l_t), longitude__range=(lng_l_t, lng_r_b), is_expert=True, is_expert_active=True)[:30]
        serializer = UserProfileSerializer(user_profile_array, many=True)
        # user_id_array = user_profile_array.values("user")
        # user_array = User.objects.filter(pk__in=user_id_array)
        # user_profile_json = serializers.serialize("json", user_profile_array, ensure_ascii=False, fields=('nick_name', 'profile_image' 'description', 'latitude', 'longitude', 'job'))
        # user_json = serializers.serialize("json", user_array, ensure_ascii=False, fields=('username', 'last_login'))
        # joined_collection = user_profile_json + '__joined_collection__' + user_json
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def update_user_info(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        is_expert = request.POST['is_expert']
        nick_name = request.POST['nick_name']
        description = request.POST['description']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location = request.POST['location']
        job = request.POST['job']
        user_profile = UserProfile.objects.get(user=request.user)

        # TODO : must delete this code..
        if int(is_expert) == 0:
            user_profile.is_expert = False
        elif int(is_expert) == 1:
            user_profile.is_expert = True
        user_profile.nick_name = nick_name
        user_profile.description = description
        user_profile.latitude = latitude
        user_profile.longitude = longitude
        user_profile.location = location
        user_profile.job = job
        user_profile.save()
        return JsonResponse({'status': 'success', 'username': request.user.username})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def update_profile_image(request):
    if request.method == "POST":
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_active:
            return JsonResponse({'status': 'error', 'error_code': '103', 'desc': 'user is not expert'})
        try:
            profile_image = request.FILES['profile_image']
        except MultiValueDictKeyError:
            return JsonResponse({'status': 'error', 'error_code': '107', 'desc': 'profile image not found'})
        # user_profile.profile_image.delete(save=False)
        user_profile.profile_image = profile_image
        user_profile.save()

        return JsonResponse({'status': 'success', 'username': request.user.username})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'fault page'})


@csrf_exempt
def follow(request, target_username):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        target_user_profile = User.objects.get(username=target_username).userprofile
        request.user.userprofile.add_relationship(target_user_profile)
        return JsonResponse({'status': 'success', 'username': request.user.username})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def un_follow(request, target_username):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        target_user_profile = User.objects.get(username=target_username).userprofile
        request.user.userprofile.remove_relationship(target_user_profile)
        return JsonResponse({'status': 'success', 'username': request.user.username})
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_follower(request, username):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        user_profile = User.objects.get(username=username).userprofile
        follower_array = user_profile.get_followers()
        # user_id_array = follower_array.values("user")
        # user_array = User.objects.filter(pk__in=user_id_array)
        # user_profile_json = serializers.serialize("json", follower_array, ensure_ascii=False, fields=('nick_name', 'profile_image' 'description', 'latitude', 'longitude', 'job'))
        # user_json = serializers.serialize("json", user_array, ensure_ascii=False, fields=('username', 'last_login'))
        # joined_collection = user_profile_json + '__joined_collection__' + user_json
        serializer = UserProfileSerializer(follower_array, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_following(request, username):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        # user_profile = User.objects.get(username=username).userprofile
        # follower_array = user_profile.get_following()
        # user_id_array = follower_array.values("user")
        # user_array = User.objects.filter(pk__in=user_id_array)
        # user_profile_json = serializers.serialize("json", follower_array, ensure_ascii=False, fields=('nick_name', 'profile_image' 'description', 'latitude', 'longitude', 'job'))
        # user_json = serializers.serialize("json", user_array, ensure_ascii=False, fields=('username', 'last_login'))
        # joined_collection = user_profile_json + '__joined_collection__' + user_json
        user_profile = User.objects.get(username=username).userprofile
        follower_queryset = user_profile.get_following()
        serializer = UserProfileSerializer(follower_queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def search_by_username(request, username):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})

    user_profile = User.objects.get(username=username).userprofile
    serializer = UserProfileSerializer(user_profile)
    # json_result = serializers.serialize('json', [user, user.userprofile, ], indent=4, fields=('username', 'profile_image', 'description', 'nick_name', 'latitude', 'longitude', 'last_login', 'job'))
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def test(request):

    queryset = UserProfile.objects.all()
    serializer = UserProfileSerializer(queryset, many=True)

    return JsonResponse(serializer.data, safe=False)
