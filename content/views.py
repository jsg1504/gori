from django.http import JsonResponse
from content.models import Content
from user_profile.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from serializer import ContentSerializer


@csrf_exempt
def new_content(request):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})

    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_expert:
            return JsonResponse({'status': 'error', 'error_code': '103', 'desc': 'user is not expert'})
        content_type = request.POST['content_type']
        content = Content.objects.create(user_profile=user_profile, content_type=content_type, is_active=False, state=1)
        return JsonResponse({'status': 'success', 'content_id': content.id, 'desc': 'content create'})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'insert new content failed'})


@csrf_exempt
def content_image_upload(request, content_id):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_expert:
            return JsonResponse({'status': 'error', 'error_code': '103', 'desc': 'user is not expert'})
        content = Content.objects.get(id=content_id)
        if content.user_profile.user_id != user_profile.user_id:
            return JsonResponse({'status': 'error', 'error_code': '105', 'desc': 'user, content mismatch'})
        if content.is_active:
            return JsonResponse({'status': 'error', 'error_code': '108', 'desc': 'already upload complete'})
        try:
            image_file = request.FILES['image_file']
        except MultiValueDictKeyError:
            return JsonResponse({'status': 'error', 'error_code': '107', 'desc': 'profile image not found'})
        if content.image_file:
            content.image_file.delete()

        content.image_file = image_file
        if content.state == 3:
            content.is_active = True
        else:
            content.state = 2
        content.save()
        return JsonResponse({'status': 'success', 'content_id': content.id, 'desc': 'image upload'})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'insert new content failed'})


@csrf_exempt
def content_description_upload(request, content_id):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_expert:
            return JsonResponse({'status': 'error', 'error_code': '103', 'desc': 'user is not expert'})
        content = Content.objects.get(id=content_id)
        if content.is_active:
            return JsonResponse({'status': 'error', 'error_code': '108', 'desc': 'already upload complete'})
        if content.user_profile.user_id != user_profile.user_id:
            return JsonResponse({'status': 'error', 'error_code': '105', 'desc': 'user, content mismatch'})
        description = request.POST['description']
        content.description = description
        if content.state == 2:
            content.is_active = True
        content.state = 3
        content.save()
        return JsonResponse({'status': 'success', 'content_id': content.id, 'desc': 'description upload'})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'insert new content failed'})


@csrf_exempt
def content_upload_cancel(request, content_id):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        content = Content.objects.get(id=content_id)
        if content.user_profile.user_id != user_profile.user_id:
            return JsonResponse({'status': 'error', 'error_code': '105', 'desc': 'user, content mismatch'})
        if content.image_file:
            content.image_file.delete()
        content.delete()
        return JsonResponse({'status': 'success', 'desc': 'description upload'})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'insert new content failed'})


@csrf_exempt
def content_delete(request, content_id):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        content = Content.objects.get(id=content_id)
        if content.user_profile.user_id != user_profile.user_id:
            return JsonResponse({'status': 'error', 'error_code': '105', 'desc': 'user, content mismatch'})
        if content.image_file:
            content.image_file.delete()
        content.delete()
        return JsonResponse({'status': 'success', 'content_id': content.id, 'desc': 'description upload'})

    return JsonResponse({'status': 'error', 'error_code': '101', 'desc': 'insert new content failed'})


@csrf_exempt
def get_content_detail(request, content_id):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error', 'error_code': '100', 'desc': 'session is not exist.'})
    if request.method == "GET":
        content = Content.objects.get(id=content_id)
        content_json = ContentSerializer(content)
        return JsonResponse(content_json.data, safe=False)
        # user = content.user
        # content_user_json = serializers.serialize('json', [user, content], fields=('username', 'profile_image', 'image_file', 'description', 'created_at', 'content_type'))
        # return JsonResponse(content_user_json, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '102', 'desc': 'content is not exist.'})


@csrf_exempt
def get_content_by_user(request, username):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        user_profile = User.objects.get(username=username).userprofile
        contents = Content.objects.filter(is_active=True, user_profile=user_profile).order_by('-created_at')#:30]
        serialize = ContentSerializer(contents, many=True)
        return JsonResponse(serialize.data, safe=False)
        # user_contents_json = serializers.serialize("json", contents, ensure_ascii=False, fields=('image_file', 'description', 'created_at', 'content_type'))
        #
        # return JsonResponse(user_contents_json, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_content_by_user_date(request, username, date):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        user_profile = User.objects.get(username=username).userprofile
        contents = Content.objects.filter(is_active=True, user_profile=user_profile, created_at__lt=date).order_by('-created_at')#[:30]
        serialize = ContentSerializer(contents, many=True)
        return JsonResponse(serialize.data, safe=False)
        # user_contents_json = serializers.serialize("json", contents, ensure_ascii=False, fields=('image_file', 'description', 'created_at', 'content_type'))
        #
        # return JsonResponse(user_contents_json, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_content_last_30(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        contents = Content.objects.filter(is_active=True).order_by('-created_at')#[:30]
        serializer = ContentSerializer(contents, many=True)
        return JsonResponse(serializer.data, safe=False)
        # contents_json = serializers.serialize('json', contents, fields=('user', 'image_file', 'description', 'created_at', 'content_type'))
        # return JsonResponse(contents_json, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_content_last_30_by_date(request, date):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        contents = Content.objects.filter(is_active=True, created_at__lt=date).order_by('-created_at')#[:30]
        serializer = ContentSerializer(contents, many=True)
        return JsonResponse(serializer.data, safe=False)
        # contents_json = serializers.serialize('json', contents, fields=('user', 'image_file', 'description', 'created_at', 'content_type'))
        # return JsonResponse(contents_json, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_content_30_by_following(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        user_profile = User.objects.get(username=request.user).userprofile
        following_user_profile_array = user_profile.get_following()
        contents = Content.objects.filter(user_profile_id__in=following_user_profile_array.values('user'), is_active=True).order_by('-created_at')#[:30]
        # following_user_profile_array = UserProfile.objects.filter(user_id__in=contents.values('user'))
        # following_user_array = User.objects.filter(id__in=following_user_profile_array.values('user'))
        # contents_json = serializers.serialize('json', contents, fields=('user', 'image_file', 'description', 'created_at', 'content_type'))
        # user_json = serializers.serialize('json', following_user_array, fields=('username', ))
        # user_profile_json = serializers.serialize('json', following_user_profile_array, fields=('profile_image', ))
        # joined_collection = contents_json + '__joined_collection__' + user_json + '__joined_collection__' + user_profile_json
        serializer = ContentSerializer(contents, many=True)
        return JsonResponse(serializer.data, safe=False)
    # return JsonResponse(joined_collection, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})


@csrf_exempt
def get_content_30_by_following_by_date(request, date):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'error', 'error': '100', 'desc': 'session is not exist.'})
        user_profile = User.objects.get(username=request.user).userprofile
        following_user_profile_array = user_profile.get_following()
        contents = Content.objects.filter(user_profile_id__in=following_user_profile_array.values('user'), is_active=True, created_at__lt=date).order_by('-created_at')#[:30]
        # following_user_profile_array = UserProfile.objects.filter(user_id__in=contents.values('user'))
        # following_user_array = User.objects.filter(id__in=following_user_profile_array.values('user'))
        # contents_json = serializers.serialize('json', contents, fields=('user', 'image_file', 'description', 'created_at', 'content_type'))
        # user_json = serializers.serialize('json', following_user_array, fields=('username', ))
        # user_profile_json = serializers.serialize('json', following_user_profile_array, fields=('profile_image', ))
        # joined_collection = contents_json + '__joined_collection__' + user_json + '__joined_collection__' + user_profile_json
        # return JsonResponse(joined_collection, safe=False)
        serializer = ContentSerializer(contents, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'error_code': '404', 'desc': 'fault page'})
