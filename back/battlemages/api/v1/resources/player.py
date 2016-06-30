from battlemages.core.players.models import Player

from rest_framework import serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api.v1:player-detail', lookup_field='pk')

    class Meta:
        model = Player
        fields = ('url', 'username', 'email', 'is_staff', 'gold')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = UserSerializer
