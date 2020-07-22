# Django imports
from django.utils import timezone

# Rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
)
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
)

# Model imports
from user.models import (
    User
)

# Serialier imports
from user.admin.serializers import (
    PublicProfileSerializer
)

# List User Profile
class UserView(generics.ListAPIView):
    model = User
    serializer_class = PublicProfileSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    search_fields = (
        'email',
    )
    filter_fields = (
        'email',
    )
    ordering_fields = (
        'email',
        'created_at'
    )

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

# Block User
class BlockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = PublicProfileSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        # Check created account time
        if user.created_at > request.user.created_at:
            Response(ErrorTemplate.AdminError.NOT_BLOCK_OLDER_ADMIN, status.HTTP_400_BAD_REQUEST)

        if user.is_active == True:
            user.__dict__.update(
                is_active=False,
                modified_by=request.user.id
            )
            user.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return user

# Unblock User
class UnblockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = PublicProfileSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        if user.is_active == False:
            user.__dict__.update(
                is_active=True,
                modified_by=request.user.id
            )
            user.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return user

# Set User to Admin
class SetAdminView(generics.RetrieveAPIView):
    model = User
    serializer_class = PublicProfileSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        user.__dict__.update(
            is_staff=True,
            modified_by=request.user.id
        )
        user.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return user

# Unset User to Admin
class UnsetAdminView(generics.RetrieveAPIView):
    model = User
    serializer_class = PublicProfileSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        user.__dict__.update(
            is_staff=False,
            modified_by=request.user.id
        )
        user.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return user