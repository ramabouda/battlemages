from rest_framework import serializers, viewsets

from elements.core.players import player_models
from .users import UserSerializer

# Serializers define the API representation.
# class PlayerSerializer(UserSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='api.v1:user-detail', lookup_field='pk')

#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')

# # ViewSets define the view behavior.
# class FriendsViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
