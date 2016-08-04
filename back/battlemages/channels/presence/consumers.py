import json

from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import enforce_ordering

import battlemages.channels.jwt_auth as channels_auth


class PresenceConsumer(JsonWebsocketConsumer):

    def get_handler(self, message, **kwargs):
        """
        Pull out the path onto an instance variable, and optionally
        adds the ordering decorator.
        """
        self.path = message['path']
        handler = getattr(self, self.method_mapping[message.channel.name])
        handler = channels_auth.jwt_request_user(handler)
        if self.strict_ordering:
            handler = enforce_ordering(handler, slight=False)
        elif self.slight_ordering:
            handler = enforce_ordering(handler, slight=True)
        return handler

    def connection_groups(self, **kwargs):
        """Define the groups joined while connected"""
        return ['presence-all']

    def connect(self, message, **kwargs):
        """Called when a WebSocket connection is opened."""
        # TODO(raph): send connected users
        message.reply_channel.send({
            'text': json.dumps({
                'some_user_id1': 'some_user_data1',
                'some_user_id2': 'some_user_data2',
            })
        })
        self.group_send('presence-all', {
            message.user.id: 'user_data_of {}'.format(message.user.username)
        })
