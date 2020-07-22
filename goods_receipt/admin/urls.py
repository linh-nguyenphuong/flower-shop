# Django imports
from django.conf.urls import url

# Application imports
from goods_receipt.admin.views import (
    GoodsReceiptView,
    GoodsReceiptDetailsView
)

urlpatterns = [
    url(r'^$', GoodsReceiptView.as_view(), name='goods-receipt-view'),
    url(r'^(?P<goods_receipt_id>[0-9]+)/$', GoodsReceiptDetailsView.as_view(), name='goods-receipt-view-details'),
]
