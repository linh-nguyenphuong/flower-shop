# Django imports
from django.conf.urls import url

# Application imports
from flower_category.admin.views import (
    FlowerCategoryView,
    FlowerCategoryDetailsView
)

urlpatterns = [
    url(r'^$', FlowerCategoryView.as_view(), name='flower-category'),
    url(r'^(?P<flower_category_id>[0-9]+)/$', FlowerCategoryDetailsView.as_view(), name='flower-category-details'),
]
