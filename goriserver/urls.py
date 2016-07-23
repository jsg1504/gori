"""goriserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from user_profile.urls import urlpatterns as profile_urls
from content.urls import urlpatterns as content_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', 'user_profile.views.login', name='login'),
    url(r'^accounts/token_csrf/', 'user_profile.views.token_csrf', name='get_token_csrf'),
    url(r'^accounts/logout/', 'user_profile.views.logout', name='logout'),
    url(r'^accounts/signup/', 'user_profile.views.sign_up', name='sign_up'),
    url(r'^accounts/(?P<username>[\w.@+-]+)/(?P<uuid>[\w.@+-]+)/$', 'user_profile.views.cert_email', name='cert_email'),
    url(r'^accounts/update/$', 'user_profile.views.update_user_info', name='update_user_info'),
    url(r'^success/', 'user_profile.views.mobile_login_after', name='success_login'),
    url(r'^user/', include(profile_urls, namespace='profiles')),
    url(r'^content/', include(content_urls, namespace='contents')),
    url(r'^test/', 'user_profile.views.test', name='test'),
]
urlpatterns += static('static_files', document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
