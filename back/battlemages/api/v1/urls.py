from django.conf.urls import url, include

from rest_framework import routers
import rest_framework_jwt.views as jwt_views

from .resources import player

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'player', player.UserViewSet)

urlpatterns = [
    url(r'^auth_token/', jwt_views.obtain_jwt_token),
    url(r'^auth_token_refresh/', jwt_views.refresh_jwt_token),
    url(r'^', include(router.urls)),
]
