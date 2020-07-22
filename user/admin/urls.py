# Django imports
from django.conf.urls import url

# Application imports
from user.admin.views import (
    UserView,
    BlockUser,
    UnblockUser,
    SetAdminView,
    UnsetAdminView
)

urlpatterns = [
    url(r'^$', UserView.as_view(), name='user-view'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/block/$', BlockUser.as_view(), name='block-user'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/unblock/$', UnblockUser.as_view(), name='unblock-user'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/set-admin/$', SetAdminView.as_view(), name='set-admin'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/unset-admin/$', UnsetAdminView.as_view(), name='unset-admin'),
]
