# Django imports
from django.utils import timezone

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError
)
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
)

# Model imports
from goods_receipt.models import GoodsReceipt
from flower.models import Flower
from supplier.models import Supplier

# Serialier imports
from goods_receipt.admin.serializers import (
    GoodsReceiptSerializer,
)

# List - Create Goods Receipt
class GoodsReceiptView(generics.ListCreateAPIView):
    model = GoodsReceipt
    serializer_class = GoodsReceiptSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    search_fields = (
        'flower__name',
    )
    filter_fields = (
        'supplier_id',
        'flower_id',
    )
    ordering_fields = (
        'created_at',
        'historical_cost',
    )

    def get_queryset(self):
        return self.model.objects.filter(
        ).order_by('created_at')

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

        # Check Supplier exists
        supplier = Supplier.objects.filter(
            id=data.get('supplier_id'),
            is_deleted=False
        ).first()
        if not supplier:
            return Response(ErrorTemplate.AdminError.SUPPLIER_NOT_EXIST)

        # Init Residual quantity
        goods_receipt = self.model(
            historical_cost=data.get('historical_cost'),
            receipt_quantity=data.get('receipt_quantity'),
            residual_quantity=data.get('receipt_quantity'),
            expired_date=data.get('expired_date'),
            flower_id=flower.id,
            supplier_id=supplier.id
        )

        # Save object
        goods_receipt.save()

        serializer = self.serializer_class(instance=goods_receipt)

        return Response({
            'success': True,
            'data': serializer.data
        })

# Retrieve - Update - Delete Goods Receipt 
class GoodsReceiptDetailsView(generics.RetrieveUpdateAPIView):
    model = GoodsReceipt
    serializer_class = GoodsReceiptSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'goods_receipt_id'

    def get(self, request, *args, **kwargs):
        goods_receipt_id = self.kwargs.get(self.lookup_url_kwarg)
        goods_receipt = self.get_object(goods_receipt_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=goods_receipt)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        goods_receipt_id = self.kwargs.get(self.lookup_url_kwarg)
        goods_receipt = self.get_object(goods_receipt_id)
        
        # Get serializer
        serializer = self.serializer_class(goods_receipt, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Flower exists
        flower = Flower.objects.filter(
            id=data.get('flower_id'),
            is_deleted=False
        ).first()
        if not flower:
            return Response(ErrorTemplate.AdminError.FLOWER_NOT_EXIST)

        # Check Supplier exists
        supplier = Supplier.objects.filter(
            id=data.get('supplier_id'),
            is_deleted=False
        ).first()
        if not supplier:
            return Response(ErrorTemplate.AdminError.SUPPLIER_NOT_EXIST)

        # Save object
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.GOODS_RECEIPT_NOT_EXIST)

        return obj








