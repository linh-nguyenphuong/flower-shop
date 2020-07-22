# Django imports
from django.conf.urls import url, include

# Application imports
from flower_category.user.views import (
    FlowerCategoryView,
    FlowerCategoryDetailsView
)

urlpatterns = [
    url(r'^$', FlowerCategoryView.as_view(), name='flower-category-user-view'),
    url(r'^(?P<slug>[0-9a-z-]+)/$', FlowerCategoryDetailsView.as_view(), name='flower-category-details-user-view'),
]
