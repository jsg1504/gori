from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^detail/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^map/(?P<latitude_l_t>\d+\.\d+)/(?P<longitude_l_t>\d+\.\d+)/(?P<latitude_r_b>\d+\.\d+)/(?P<longitude_r_b>\d+\.\d+)/$', views.get_user_list_by_distance, name='user_info_by_distance'),
    url(r'^follow/(?P<target_username>[\w.@+-]+)/$', views.follow, name='request_follow'),
    url(r'^un_follow/(?P<target_username>[\w.@+-]+)/$', views.un_follow, name='request_un_follow'),
    url(r'^get/follower/(?P<username>[\w.@+-]+)/$', views.get_follower, name='get_follower'),
    url(r'^get/following/(?P<username>[\w.@+-]+)/$', views.get_following, name='get_following'),
    url(r'^update/profile_image/$', views.update_profile_image, name='update_profile_image'),
    url(r'^search/username/(?P<username>[\w.@+-]+)/$', views.search_by_username, name='search_by_username'),
    url(r'^my_info/$', views.my_info, name='my_info'),
    url(r'^detail2/(?P<username>[\w.@+-]+)/$', views.get_profile_detail, name='get_profile_detail')
]
