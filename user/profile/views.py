# Python imports
from PIL import Image

# Django imports
from django.utils import timezone

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError,
)
from rest_framework import generics

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsUser,
)

# Model imports
from user.models import (
    User
)

# Serialier imports
from user.profile.serializers import (
    ProfileSerializer
)

# Detail - Update Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = ProfileSerializer
    permission_classes = (IsUser,)

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request.user.id)
        serializer = self.serializer_class(instance=profile)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        profile = self.get_profile(request.user.id)
        serializer = self.serializer_class(instance=profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Update Profile
        profile.__dict__.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            DOB=data.get('DOB'),
            address=data.get('address')
        )
        profile.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_profile(self, user_id):
        profile = self.model.objects.filter(
            id=user_id
        ).first()

        if not profile:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return profile

# Upload User's avatar
class UploadUserAvatarView(generics.CreateAPIView):
    model = User
    serializer_class = ProfileSerializer
    permission_classes = (IsUser,)

    def post(self, request, *args, **kwargs):
        ids_response = []
        file = request.FILES.get('image')
        if not file:
            return Response(ErrorTemplate.UserError.IMAGE_REQUIRED, status.HTTP_400_BAD_REQUEST)

        # Check file type
        FORMAT = ['JPEG', 'PNG', 'BMP', 'PPM']
        img = Image.open(file)
        if img.format not in FORMAT:
            return Response(ErrorTemplate.UserError.INVALID_IMAGE, status.HTTP_400_BAD_REQUEST)
    
        profile = self.get_profile(self.request.user.id)
        profile.avatar = file
        profile.save()

        serializer = self.serializer_class(profile)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_profile(self, user_id):
        profile = self.model.objects.filter(
            id=user_id
        ).first()

        if not profile:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return profile