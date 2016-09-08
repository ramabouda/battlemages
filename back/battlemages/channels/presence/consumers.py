from ..default_consumers import AuthenticatedGroupConsumer


class PresenceConsumer(AuthenticatedGroupConsumer):
    stream_name = 'presence'

    def connection_groups(self, **kwargs):
        """Define the groups joined while connected"""
        return ['presence-all']

    def connect(self, message, **kwargs):
        """Called when a WebSocket connection is opened."""
        # TODO(raph): send connected users
        self.send({
            'some_user_id1': 'some_user_dataqsdfqsdf1',
            'some_user_id2': 'some_user_data2',
        })

        message.user.connected = True
        message.user.save()

        self.group_send('presence-all', {
            message.user.id: 'user_data_of {}'.format(message.user.username)
        })

    def disconnect(self, message, **kwargs):
        """Inform other users of the deconnection"""
        message.user.connected = False
        message.user.save()

        self.group_send('presence-all', {
            'disconnect': message.user.id,
        })

    def receive(self, text=None, bytes=None, **kwargs):
        print(text)

    @classmethod
    def get_user_data(cls, user):
        return {
            'username': user.username,
            'connected': user.connected,
        }
