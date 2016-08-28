from django.contrib import auth

from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import views

from .resources import player


class QuietBasicAuthentication(BasicAuthentication):
    """
    Used only at login
    """

    def authenticate_header(self, request):
        """
        By default with Basic authentication if user provides wrong credentials
        the browser prompts the user for their credentials again using a native
        dialogue box. Rather ugly and bad user experience. To avoid this we ensure
        the schema returns a custom value other than 'Basic'.
        """
        return 'xBasic realm="%s"' % self.www_authenticate_realm


class AuthView(views.APIView):
    authentication_classes = [QuietBasicAuthentication]
    serializer_class = player.PlayerSerializer

    def post(self, request):
        """Authenticate with the auth classes, then gives user data"""
        auth.login(request, request.user)
        return Response({'sessionid': request.session.session_key})
