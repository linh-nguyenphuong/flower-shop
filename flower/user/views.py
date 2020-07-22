# Python imports

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
from flower.models import (
    Flower,
    FlowerImage
)
from flower_category.models import FlowerCategory

# Serialier imports
from flower.user.serializers import (
    FlowerSerializer,
    FlowerImageSerializer
)

# List Flower
class FlowerView(generics.ListAPIView):
    model = Flower
    serializer_class = FlowerSerializer
    permission_classes = ()
    pagination_class = PageNumberPagination
    search_fields = (
        'name',
    )
    filter_fields = {
        'price': ['gte', 'lte'],
        'flower_category_id': ['exact'],
        'flower_category__slug': ['exact'],
    }
    ordering_fields = (
        'id',
        'name',
        'price'
    )

    def get_queryset(self):
        return self.model.objects.filter(
            is_deleted=False
        ).order_by('name')

# Retrieve Flower
class FlowerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Flower
    serializer_class = FlowerSerializer
    permission_classes = ()
    lookup_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        flower = self.get_object(slug)
        
        # Get serializer
        serializer = self.serializer_class(instance=flower)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_object(self, slug):
        obj = self.model.objects.filter(
            slug=slug,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.FLOWER_NOT_EXIST)

        return obj
