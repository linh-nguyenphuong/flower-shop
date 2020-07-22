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
    IsAdmin,
)

# Model imports
from shipping.models import (
    Shipping
)

# Serialier imports
from shipping.admin.serializers import (
    ShippingSerializer,
)

# List Shipping
class ShippingView(generics.ListAPIView):
    model = Shipping
    serializer_class = ShippingSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_fields = (
        'ship_date',
        'is_shipped'
    )
    ordering_fields = (
        'id',
        'ship_date',
    )

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

# Retrieve - Update Shipping
class ShippingDetailsView(generics.RetrieveUpdateAPIView):
    model = Shipping
    serializer_class = ShippingSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'shipping_id'

    def get(self, request, *args, **kwargs):
        shipping_id = self.kwargs.get(self.lookup_url_kwarg)
        shipping = self.get_object(shipping_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=shipping)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def patch(self, request, *args, **kwargs):
        shipping_id = self.kwargs.get(self.lookup_url_kwarg)
        shipping = self.get_object(shipping_id)
        
        # Get serializer
        serializer = self.serializer_class(shipping, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

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
            raise ValidationError(ErrorTemplate.AdminError.SHIPPING_NOT_EXIST)

        return obj








