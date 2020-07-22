# Django imports
from django.conf.urls import url

# Application imports
from order_detail.user.views import (
    OrderDetailView,
    OrderDetailDetailsView,
)

urlpatterns = [
    url(r'^$', OrderDetailView.as_view(), name='order-detail'),
    url(r'^(?P<order_detail_id>[0-9]+)/$', OrderDetailDetailsView.as_view(), name='order-detail-details'),
]
