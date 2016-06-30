from rest_framework import filters
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework import serializers


class CursorPagination(pagination.CursorPagination):
    page_size = 50


class HyperlinkedModelSerializerWithPk(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()


class ReadOnlyListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    """Readonly list and retrieve ViewSet with action customisable serializer.
    This viewset enables to have one common serializer for 'list' and 'retrieve'.
    The fields to be displayed for each action is specified by the class attributes
    `list_fields` and `retrieve_fields`.

    Allows to get more fields by using the parameter "with=field1,field2" in the query.
    """

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = CursorPagination
    ordering_fields = '__all__'
    ordering = 'pk'

    # permission_classes = (PermissionRequired,)
    permission_required = None  # Should be overridden

    lookup_field = 'pk'
    base_fields = ('url', 'uid')  # Only used on read
    list_fields = ()
    retrieve_fields = ()

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs['context'] = self.get_serializer_context()
    #     if issubclass(serializer_class, serializers.HyperlinkedModelSerializer):
    #         # action_fields = (
    #         #     getattr(self, '{action}_fields'.format(action=self.action), ())
    #         #     if self.action in ('list', 'retrieve', 'create', 'update', 'partial_update') else
    #         #     ()
    #         # )
    #         action_fields = serializer_class.Meta.fields
    #         extra_fields = ()
    #         if self.action in ('list', 'retrieve'):
    #             extra_fields = (
    #                 self.base_fields +
    #                 tuple(f for f in self.request.query_params.get('with', '').split(',') if f)
    #             )
    #         computed_fields = tuple(kwargs.get('fields', ())) + action_fields + extra_fields
    #         kwargs['fields'] = computed_fields
    #     return serializer_class(*args, **kwargs)
