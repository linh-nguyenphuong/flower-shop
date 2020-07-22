# Python imports
import jwt
from datetime import datetime

# Django imports
from django.conf import settings
from rest_framework import authentication, exceptions

# Model imports
from user.models import User

class JWTAuthentication(authentication.SessionAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(
                jwt=token, 
                key=settings.SECRET_KEY, 
                algorithms='HS256'
            )   
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        # Check token type
        if not payload.get('token_type') == 'access':
            msg = 'The token must be access token.'
            raise exceptions.AuthenticationFailed(msg)
        
        # Check token expired
        if datetime.now() > datetime.strptime(payload.get('expired_at'), '%c'):
            msg = 'The token has expired.'
            raise exceptions.AuthenticationFailed(msg)

        # Check user exist
        user = User.objects.filter(pk=payload.get('user_id')).first()
        if not user:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        # Check user account is blocked
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

    def authenticate_header(self, request):
        return 'Session'