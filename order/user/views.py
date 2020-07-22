# Python imports
from datetime import datetime

# Django imports

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed
)
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsUser,
)

# Model imports
from order.models import Order
from goods_receipt.models import GoodsReceipt
from shipping.models import Shipping

# Serialier imports
from order.user.serializers import OrderSerializer

# List History Order by their owner
class HistoryOrderView(generics.ListAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    ordering_fields = (
        'id',
        'created_at',
        'total',
    )

    def get_queryset(self):
        return self.model.objects.filter(
            checkout=True,
            customer_id=self.request.user.id
        ).order_by('id')

# Retrieve Order 
class OrderDetailsView(generics.RetrieveAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)
    lookup_url_kwarg = 'order_id'

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get(self.lookup_url_kwarg)
        order = self.get_object(order_id)

        if not order.customer_id == self.request.user.id:
            return Response(ErrorTemplate.UserError.CANNOT_SHOW_ORDER_BELONG_OTHER_PERSON)
        
        # Get serializer
        serializer = self.serializer_class(instance=order)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.ORDER_NOT_EXIST)

        return obj

# Get Current Order 
class CurrentOrderView(generics.RetrieveAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)

    def get(self, request, *args, **kwargs):
        order = self.model.objects.filter(
            checkout=False,
            customer_id=self.request.user.id
        ).order_by('-id').first()
        
        # Get serializer
        serializer = self.serializer_class(instance=order)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

# Checkout
class Checkout(APIView):
    permission_classes = (IsUser,)

    def post(self, request, *args, **kwargs):
        if not request.data.get('ship_date'):
            return Response(ErrorTemplate.UserError.SHIP_DATE_REQUIRED)
        if not request.data.get('address'):
            return Response(ErrorTemplate.UserError.ADDRESS_REQUIRED)

        order = Order.objects.filter(
            customer_id=self.request.user.id,
            checkout=False
        ).first()
        if not order:
            return Response(ErrorTemplate.UserError.EMPTY_ORDER)

        # Update Flower stock
        for order_detail in order.order_detail_order.all():
            goods_receipt = GoodsReceipt.objects.filter(
                flower_id=order_detail.flower_id,
                is_active=True,
                expired_date__gte=datetime.now().date()
            ).order_by('created_at').first()

            goods_receipt.residual_quantity -= order_detail.quantity

            if goods_receipt.residual_quantity == 0:
                goods_receipt.is_active = False
            goods_receipt.save()

        # Create Shipping record
        Shipping.objects.create(
            ship_date=request.data.get('ship_date'),
            address=request.data.get('address'),
            order_id=order.id
        )

        # Update Order
        order.checkout = True
        order.save()

        return Response({
            'success': True,
        })