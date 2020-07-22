# Django imports
from django.conf.urls import url, include

# Application imports
from user.auth.views import (
    SignUpView,
    LoginView,
    RefreshTokenView,
    ChangePasswordView,
    VerifyEmailView,
    ForgotPasswordView,
    ForgotPasswordDetailsView
)

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),
    url(r'^verify-email/(?P<token>[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)/$', VerifyEmailView.as_view(), name='verify-email'),
    url(r'^refresh-token/$', RefreshTokenView.as_view(), name='refresh-token'),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='forgot-password'),
    url(r'^forgot-password/(?P<token>[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)/$', ForgotPasswordDetailsView.as_view(), name='forgot-password-details'),
]
