from django.conf.urls import url, include
from .views import (
    index
)
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    url(r'^$', index),
    
    #Authentication
    url(r'^api/auth/', include('user.auth.urls'), name='api-auth'),

    #------------------------------------------------------
    #                     Admin API                       
    #------------------------------------------------------
    # User
    url(r'^api/admin/manage-user/', include('user.admin.urls'), name='api-admin-user'),

    # Flower Category
    url(r'^api/admin/flower-category/', include('flower_category.admin.urls'), name='api-admin-flower-category'),

    # Flower
    url(r'^api/admin/flower/', include('flower.admin.urls'), name='api-admin-flower'),

    # Supplier
    url(r'^api/admin/supplier/', include('supplier.admin.urls'), name='api-admin-supplier'),

    # Goods Receipt
    url(r'^api/admin/goods-receipt/', include('goods_receipt.admin.urls'), name='api-admin-goods-receipt'),

    # Shipping
    url(r'^api/admin/shipping/', include('shipping.admin.urls'), name='api-admin-shipping'),

    # Statistic
    url(r'^api/admin/statistic/', include('statistic.admin.urls'), name='api-admin-statistic'),

    #------------------------------------------------------
    #                     User API                       
    #------------------------------------------------------
    # Profile
    url(r'^api/user/profile/', include('user.profile.urls'), name='api-user-profile'),

    # Flower Category
    url(r'^api/user/flower-category/', include('flower_category.user.urls'), name='api-user-flower-category'),

    # Flower
    url(r'^api/user/flower/', include('flower.user.urls'), name='api-user-flower'),

    # Order Detail
    url(r'^api/user/order-detail/', include('order_detail.user.urls'), name='api-user-order-detail'),

    # Order
    url(r'^api/user/order/', include('order.user.urls'), name='api-user-order'),
]   

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)