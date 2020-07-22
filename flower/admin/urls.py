# Django imports
from django.conf.urls import url

# Application imports
from flower.admin.views import (
    FlowerView,
    FlowerDetailsView,
    UploadFlowerImageView
)

urlpatterns = [
    url(r'^$', FlowerView.as_view(), name='flower-category'),
    url(r'^upload-image/$', UploadFlowerImageView.as_view(), name='upload-flower-image'),
    url(r'^(?P<flower_id>[0-9]+)/$', FlowerDetailsView.as_view(), name='flower-details'),
]
