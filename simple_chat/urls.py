from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import logout

from rest_framework.urlpatterns import format_suffix_patterns

from chat_app.views import *


urlpatterns = [
    url(r'^$', login_redirect, name='login_redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^messenger/$', index),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),

    url(r'^api/users_list/$', UsersList.as_view(), name='users_list'),
    url(r'^api/msgs_logs/$', MessagesList.as_view(), name='msgs_logs'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
