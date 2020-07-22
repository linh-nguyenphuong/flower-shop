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
from order_detail.models import OrderDetail
from order.models import Order
from flower.models import Flower
from goods_receipt.models import GoodsReceipt

# Serialier imports
from order_detail.user.serializers import OrderDetailSerializer

# List - Create Order Detail
class OrderDetailView(generics.ListCreateAPIView):
    model = OrderDetail
    serializer_class = OrderDetailSerializer
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    search_fields = (
        'flower__name',
    )
    filter_fields = {
        'unit_price': ['gte', 'lte'],
        'order_id': ['exact'],
        'flower_id': ['exact'],
        'flower__slug': ['exact'],
    }
    ordering_fields = (
        'id',
        'unit_price'
    )

    def get_queryset(self):
        return self.model.objects.filter(
            order__customer_id=self.request.user.id
        ).order_by('id')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Flower exists
        flower = Flower.objects.filter(
            id=data.get('flower_id'),
            is_deleted=False
        ).first()
        if not flower:
            return Response(ErrorTemplate.AdminError.FLOWER_NOT_EXIST)

        # Check Flower inventory
        goods_receipt = GoodsReceipt.objects.filter(
            flower_id=flower.id,
            is_active=True,
            expired_date__gte=datetime.now().date()
        ).order_by('created_at').first()
        if not goods_receipt:
            return Response(ErrorTemplate.UserError.FLOWER_OUT_OF_STOCK)

        # Check Stock quantity after ordering 
        if goods_receipt.residual_quantity - data.get('quantity') < 0:
            return Response(ErrorTemplate.UserError.STOCK_QUANTITY_NOT_ENOUGH)

        # Get Order
        order = Order.objects.filter(
            customer_id=request.user.id,
            checkout=False
        ).first()
        if not order:
            order = Order(
                customer_id=request.user.id
            )
            order.save()

        order_detail = self.model(
            quantity=data.get('quantity'),
            unit_price=flower.price,
            flower_id=flower.id,
            order_id=order.id
        )
        # Save to database
        order_detail.save()

        # Update Order total
        order.total += order_detail.unit_price * order_detail.quantity
        order.save()

        serializer = self.serializer_class(instance=order_detail)

        return Response({
            'success': True,
            'data': serializer.data
        })

# Retrieve - Update Delete Order Detail
class OrderDetailDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = OrderDetail
    serializer_class = OrderDetailSerializer
    permission_classes = (IsUser,)
    lookup_url_kwarg = 'order_detail_id'

    def get(self, request, *args, **kwargs):
        order_detail_id = self.kwargs.get(self.lookup_url_kwarg)
        order_detail = self.get_object(order_detail_id)

        # Check user is their owner
        if not order_detail.order.customer_id == self.request.user.id:
            return Response(ErrorTemplate.UserError.CANNOT_SHOW_ORDER_BELONG_OTHER_PERSON)
        
        # Get serializer
        serializer = self.serializer_class(instance=order_detail)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        order_detail_id = self.kwargs.get(self.lookup_url_kwarg)
        order_detail = self.get_object(order_detail_id)

        # Check user is their owner
        if not order_detail.order.customer_id == self.request.user.id:
            return Response(ErrorTemplate.UserError.CANNOT_SHOW_ORDER_BELONG_OTHER_PERSON)
        
        # Get serializer
        serializer = self.serializer_class(order_detail, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if order_detail.order.checkout == True:
            return Response(ErrorTemplate.UserError.CANNOT_UPDATE_ORDER_ALREADY_CHECK_OUT)

        # Check Flower exists
        flower = Flower.objects.filter(
            id=data.get('flower_id'),
            is_deleted=False
        ).first()
        if not flower:
            return Response(ErrorTemplate.AdminError.FLOWER_NOT_EXIST)

        data.get('quantity')
        # Check Stock quantity after updating
        if order_detail.quantity < data.get('quantity'):
            # Check Flower inventory
            goods_receipt = GoodsReceipt.objects.filter(
                flower_id=flower.id,
                is_active=True,
                expired_date__gte=datetime.now().date()
            ).order_by('created_at').first()
            if not goods_receipt:
                return Response(ErrorTemplate.UserError.FLOWER_OUT_OF_STOCK)

            # Check Stock quantity after updating 
            if goods_receipt.residual_quantity < data.get('quantity') - order_detail.quantity:
                return Response(ErrorTemplate.UserError.STOCK_QUANTITY_NOT_ENOUGH)
        
        # Get Order
        order = Order.objects.filter(
            customer_id=request.user.id,
            checkout=False
        ).first()

        # Update Order total
        if order_detail.quantity < data.get('quantity'):
            order.total += order_detail.unit_price * (data.get('quantity') - order_detail.quantity)
            order.save()
        if order_detail.quantity > data.get('quantity'):
            order.total -= order_detail.unit_price * (order_detail.quantity - data.get('quantity'))
            order.save()

        order_detail.__dict__.update(
            quantity=data.get('quantity'),
            flower_id=flower.id
        )
        
        # Save to database
        order_detail.save()

        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def delete(self, request, *args, **kwargs):
        order_detail_id = self.kwargs.get(self.lookup_url_kwarg)
        order_detail = self.get_object(order_detail_id)

        # Check user is their owner
        if not order_detail.order.customer_id == self.request.user.id:
            return Response(ErrorTemplate.UserError.CANNOT_SHOW_ORDER_BELONG_OTHER_PERSON)

        if order_detail.order.checkout == True:
            return Response(ErrorTemplate.UserError.CANNOT_DELETE_ORDER_ALREADY_CHECK_OUT)
        
        # Get Order
        order = Order.objects.filter(
            customer_id=request.user.id,
            checkout=False
        ).first()

        # Update Order total
        order.total -= order_detail.unit_price * order_detail.quantity
        order.save()

        order_detail.delete()

        return Response({
            'success': True
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.ORDER_DETAIL_NOT_EXIST)

        return obj



