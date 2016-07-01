from channels.generic.websockets import JsonWebsocketConsumer

class PresenceConsumer(JsonWebsocketConsumer):

    def connection_groups(self, **kwargs):
        """Define the groups joined while connected"""
        return ['presence-all']

    def connect(self, message, **kwargs):
        """Called when a WebSocket connection is opened."""
        self.group_send('presence-all', 'A user joined on port {0}'.format(message.content['client'][1]))
