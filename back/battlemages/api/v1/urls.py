from django.conf.urls import url, include

from rest_framework import routers

from .resources import player
from . import authentication

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'player', player.PlayerViewSet)

urlpatterns = [
    url(r'authentication', authentication.AuthView.as_view()),
    url(r'^', include(router.urls)),
]
