# Django imports
from django.conf.urls import url

# Application imports
from shipping.admin.views import (
    ShippingView,
    ShippingDetailsView
)

urlpatterns = [
    url(r'^$', ShippingView.as_view(), name='shipping'),
    url(r'^(?P<shipping_id>[0-9]+)/$', ShippingDetailsView.as_view(), name='shipping-details'),
]
