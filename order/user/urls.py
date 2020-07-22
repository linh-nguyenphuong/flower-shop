# Django imports
from django.conf.urls import url

# Application imports
from order.user.views import (
    HistoryOrderView,
    OrderDetailsView,
    CurrentOrderView,
    Checkout
)

urlpatterns = [
    url(r'^history/$', HistoryOrderView.as_view(), name='order-user-view'),
    url(r'^current/$', CurrentOrderView.as_view(), name='current-order-user-view'),
    url(r'^(?P<order_id>[0-9]+)/$', OrderDetailsView.as_view(), name='order-details-user-view'),
    url(r'^checkout/$', Checkout.as_view(), name='checkout-user-view'),
]
