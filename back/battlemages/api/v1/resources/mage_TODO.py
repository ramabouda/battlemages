from rest_framework import serializers

import elements.api.helpers as api_helpers

from elements.core.cards.models import Hero
from .cards import EnergyTypeSerializer


class HeroSerializer(api_helpers.HyperlinkedModelSerializerWithPk):
    url = serializers.HyperlinkedIdentityField(view_name='api.v1:hero-detail', lookup_field='pk', read_only=True)
    elements = EnergyTypeSerializer(many=True)

    class Meta:
        model = Hero
        fields = '__all__'


class HeroViewSet(api_helpers.ReadOnlyListRetrieveViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
