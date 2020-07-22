# Django imports
from django.conf.urls import url

# Application imports
from supplier.admin.views import (
    SupplierView,
    SupplierDetailsView
)

urlpatterns = [
    url(r'^$', SupplierView.as_view(), name='supplier-view'),
    url(r'^(?P<supplier_id>[0-9]+)/$', SupplierDetailsView.as_view(), name='supplier-view-details'),
]
