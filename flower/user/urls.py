# Django imports
from django.conf.urls import url

# Application imports
from flower.user.views import (
    FlowerView,
    FlowerDetailsView
)

urlpatterns = [
    url(r'^$', FlowerView.as_view(), name='flower-category-user-view'),
    url(r'^(?P<slug>[0-9a-z-]+)/$', FlowerDetailsView.as_view(), name='flower-details-user-view'),
]
