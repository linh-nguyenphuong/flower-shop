# Django imports
from django.conf.urls import url, include

# Application imports
from user.profile.views import (
    ProfileView,
    UploadUserAvatarView
)

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile-user-view'),
    url(r'^avatar/$', UploadUserAvatarView.as_view(), name='upload-user-avatar'),
]
