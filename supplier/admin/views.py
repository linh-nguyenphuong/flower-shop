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
from supplier.models import (
    Supplier
)

# Serialier imports
from supplier.admin.serializers import (
    SupplierSerializer,
)

# List - Create Supplier
class SupplierView(generics.ListCreateAPIView):
    model = Supplier
    serializer_class = SupplierSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    search_fields = (
        'name',
    )
    filter_fields = (
        'name',
    )
    ordering_fields = (
        'name',
    )

    def get_queryset(self):
        return self.model.objects.filter(
            is_deleted=False
        ).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Supplier exists
        is_existed = self.model.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exists()
        if is_existed:
            return Response(ErrorTemplate.AdminError.SUPPLIER_ALREADY_EXISTED, status.HTTP_400_BAD_REQUEST)

        # Save object
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

# Retrieve - Update - Delete Supplier 
class SupplierDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Supplier
    serializer_class = SupplierSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'supplier_id'

    def get(self, request, *args, **kwargs):
        supplier_id = self.kwargs.get(self.lookup_url_kwarg)
        supplier = self.get_object(supplier_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=supplier)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        supplier_id = self.kwargs.get(self.lookup_url_kwarg)
        supplier = self.get_object(supplier_id)
        
        # Get serializer
        serializer = self.serializer_class(supplier, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Supplier exists
        supplier_is_existed = self.model.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exclude(id=supplier_id).exists()
        if supplier_is_existed:
            raise ValidationError(ErrorTemplate.AdminError.SUPPLIER_ALREADY_EXISTED)

        # Save object
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def delete(self, request, *args, **kwargs):
        supplier_id = self.kwargs.get(self.lookup_url_kwarg)
        supplier = self.get_object(supplier_id)

        supplier.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        supplier.save()

        return Response({
            'success': True
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.SUPPLIER_NOT_EXIST)

        return obj








