from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload1/$', views.new_content, name='new_content'),
    url(r'^upload2/(?P<content_id>\d+)/$', views.content_image_upload, name='image_upload'),
    url(r'^upload3/(?P<content_id>\d+)/$', views.content_description_upload, name='description_upload'),
    url(r'^upload/cancel/(?P<content_id>\d+)/$', views.content_upload_cancel, name='content_upload_cancel'),
    url(r'^delete/(?P<content_id>\d+)/$', views.content_delete, name='content_delete'),
    url(r'^get/detail/(?P<content_id>\d+)/$', views.get_content_detail, name='get_content_detail'),
    url(r'^get/by/user/(?P<username>[\w.@+-]+)/$', views.get_content_by_user, name='get_content_by_user'),
    url(r'^get/by/user/(?P<username>[\w.@+-]+)/date/(?P<date>[\w.:@+-]+)/$', views.get_content_by_user_date, name='get_content_by_user_date'),
    url(r'^get/all/last/$', views.get_content_last_30, name='get_content_last_30'),
    url(r'^get/by/following/$', views.get_content_30_by_following, name='get_content_30_by_following'),
    url(r'^get/all/last/date/(?P<date>[\w.:@+-]+)/$', views.get_content_last_30_by_date, name='get_content_last_30_by_date'),
    url(r'^get/by/following/date/(?P<date>[\w.:@+-]+)/$', views.get_content_30_by_following_by_date, name='get_content_30_by_following_by_date'),
]
