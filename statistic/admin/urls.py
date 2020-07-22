# Django imports
from django.conf.urls import url

# Application imports
from statistic.admin.views import (
    RevenueStatisticView,
    FlowerStatisticView
)

urlpatterns = [
    url(r'^revenue/$', RevenueStatisticView.as_view(), name='revenue-statistic-view'),
    url(r'^flower/$', FlowerStatisticView.as_view(), name='flower-statistic-view'),
]
