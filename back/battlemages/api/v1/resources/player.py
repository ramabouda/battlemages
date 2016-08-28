from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets

from battlemages.core.players.models import Player


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """Allow user to list all users if logged in user is staff"""
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """Allow logged in user to view own details, allows staff to view all records"""
        return request.user.is_staff or obj == request.user


# Serializers define the API representation.
class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api.v1:player-detail', lookup_field='pk')

    class Meta:
        model = Player
        write_only_fields = ('password',)
        fields = ('url', 'username', 'email', 'is_staff', 'gold')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def restore_object(self, attrs, instance=None):
        """Call set_password on user object. Without this the password will be stored in plain text."""
        user = super(PlayerSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

# ViewSets define the view behavior.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    # def get_permissions(self):
    #     """Allow non-authenticated user to create via POST"""
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else IsStaffOrTargetUser()),
