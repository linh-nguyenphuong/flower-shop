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
from flower_category.models import (
    FlowerCategory
)

# Serialier imports
from flower_category.user.serializers import (
    FlowerCategorySerializer,
)

# List Flower Category
class FlowerCategoryView(generics.ListAPIView):
    model = FlowerCategory
    serializer_class = FlowerCategorySerializer
    permission_classes = ()
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

# Retrieve Flower Category
class FlowerCategoryDetailsView(generics.RetrieveAPIView):
    model = FlowerCategory
    serializer_class = FlowerCategorySerializer
    permission_classes = ()
    lookup_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        flower_category = self.get_object(slug)
        
        # Get serializer
        serializer = self.serializer_class(instance=flower_category)
        
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
            raise ValidationError(ErrorTemplate.AdminError.FLOWER_CATEGORY_NOT_EXIST)

        return obj








