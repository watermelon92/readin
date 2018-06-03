"""readin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from docs import views as home_views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    url(r'^$', home_views.home, name='home'),
    url(r'^docs/$', home_views.docs, name='docs'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^docs/upload/$', home_views.upload, name='upload'),
    url(r'^docs/edit/(?P<id>\d+)/$', home_views.edit, name='editDoc'),
    url(r'^docs/delete/(?P<id>\d+)/$',home_views.delete,name='deleteDoc'),
    url(r'^admin/', admin.site.urls),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^uploadedfiles/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        },name='storage'),
    ]