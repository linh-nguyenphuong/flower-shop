# Python imports
from PIL import Image

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
from flower.models import (
    Flower,
    FlowerImage
)
from flower_category.models import FlowerCategory

# Serialier imports
from flower.admin.serializers import (
    FlowerSerializer,
    FlowerImageSerializer
)

# List - Create Flower
class FlowerView(generics.ListCreateAPIView):
    model = Flower
    serializer_class = FlowerSerializer
    permission_classes = (IsAdmin,)
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

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Flower exists
        is_existed = self.model.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exists()
        if is_existed:
            return Response(ErrorTemplate.AdminError.FLOWER_ALREADY_EXISTED, status.HTTP_400_BAD_REQUEST)

        # Check Flower Category exists
        flower_category = FlowerCategory.objects.filter(
            id=data.get('flower_category_id'),
            is_deleted=False
        ).first()
        if not flower_category:
            return Response(ErrorTemplate.AdminError.FLOWER_CATEGORY_NOT_EXIST)

        flower = Flower(
            name=data.get('name'),
            price=data.get('price'),
            detail=data.get('detail'),
            flower_category_id=flower_category.id
        )
        # Save to database
        flower.save()

        # Add Flower images
        image_ids = request.data.get('image_ids')
        if not image_ids:
            raise ValidationError(ErrorTemplate.UserError.IMAGE_REQUIRED)
        
        set_main_image = False
        for image_id in image_ids:
            image = FlowerImage.objects.filter(
                id=image_id
            ).first()
            if not image:
                raise ValidationError(ErrorTemplate.UserError.IMAGE_NOT_EXIST)
            image.flower_id = flower.id

            if not set_main_image:
                image.is_main = True
                set_main_image = True
            image.save()

        serializer = self.serializer_class(instance=flower)

        return Response({
            'success': True,
            'data': serializer.data
        })

# Retrieve - Update - Delete Flower
class FlowerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Flower
    serializer_class = FlowerSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'flower_id'

    def get(self, request, *args, **kwargs):
        flower_id = self.kwargs.get(self.lookup_url_kwarg)
        flower = self.get_object(flower_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=flower)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        flower_id = self.kwargs.get(self.lookup_url_kwarg)
        flower = self.get_object(flower_id)
        
        # Get serializer
        serializer = self.serializer_class(flower, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Flower exists
        is_existed = self.model.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exclude(
            id=flower.id
        ).exists()
        if is_existed:
            return Response(ErrorTemplate.AdminError.FLOWER_ALREADY_EXISTED, status.HTTP_400_BAD_REQUEST)

        # Check Flower Category exists
        flower_category = FlowerCategory.objects.filter(
            id=data.get('flower_category_id'),
            is_deleted=False
        ).first()
        if not flower_category:
            return Response(ErrorTemplate.AdminError.FLOWER_CATEGORY_NOT_EXIST)

        flower.__dict__.update(
            name=data.get('name'),
            price=data.get('price'),
            detail=data.get('detail'),
            flower_category_id=flower_category.id
        )

        # Update Flower's images
        image_ids = request.data.get('image_ids')
        if not image_ids:
            raise ValidationError(ErrorTemplate.UserError.IMAGE_REQUIRED)
        
        for image_id in image_ids:
            image = FlowerImage.objects.filter(
                id=image_id
            ).first()
            if not image:
                raise ValidationError(ErrorTemplate.UserError.IMAGE_NOT_EXISTED)
            
        images = FlowerImage.objects.filter(
            flower_id=flower.id
        )

        set_main_image = True
        # Delete Flower's images
        for image in images:
            if str(image.id) not in image_ids:
                if image.is_main:
                    set_main_image = False
                image.delete()
        
        # Add new Flower's images
        for image_id in image_ids:
            image = FlowerImage.objects.get(
                id=image_id
            )
            image.flower_id = flower.id
            
            if not set_main_image:
                image.is_main = True
                set_main_image = True  
            image.save() 

        # Save to database
        flower.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def delete(self, request, *args, **kwargs):
        flower_id = self.kwargs.get(self.lookup_url_kwarg)
        flower = self.get_object(flower_id)

        flower.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        flower.save()

        return Response({
            'success': True
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.FLOWER_NOT_EXIST)

        return obj

# Upload Flower's images
class UploadFlowerImageView(generics.CreateAPIView):
    model = FlowerImage
    serializer_class = FlowerImageSerializer
    permission_classes = (IsAdmin,)

    def post(self, request, *args, **kwargs):
        ids_response = []
        files = request.FILES.getlist('images[]')
        if not files:
            return Response(ErrorTemplate.UserError.IMAGE_REQUIRED, status.HTTP_400_BAD_REQUEST)

        # Check file type
        FORMAT = ['JPEG', 'PNG', 'BMP', 'PPM']
        for file in files:
            img = Image.open(file)
            if img.format not in FORMAT:
                return Response(ErrorTemplate.UserError.INVALID_IMAGE, status.HTTP_400_BAD_REQUEST)
    
        for file in files: 
            image = self.model(
                url=file,
            )
            ids_response.append(image.id)

            # Save object
            image.save()

        return Response({
            'success': True,
            'image_ids': ids_response
        })





