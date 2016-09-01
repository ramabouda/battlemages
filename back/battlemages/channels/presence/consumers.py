import json

from channels.generic.websockets import JsonWebsocketConsumer
from channels.auth import channel_session_user, channel_session_user_from_http
from channels import Group

from ..demultiplexer import Demultiplexer

@channel_session_user
def presence_consumer(message):
    print(message)

@channel_session_user_from_http
def connect_consumer(message):
    message.reply_channel.send({
        'text': json.dumps({
            'some_user_id1': 'some_user_data1',
            'some_user_id2': 'some_user_data2',
        })
    })
    # Demultiplexer.send()

    message.user.connected = True
    message.user.save()

    Group('presence-all').add(message.reply_channel)
    Group('presence-all').send({
        'text': json.dumps({
            message.user.id: 'user_data_of {}'.format(message.user.username)
        })
    })



# class PresenceConsumer(JsonWebsocketConsumer):
#     http_user = True

#     # def channel_names():
#     #     """Channels that we listen to ?"""
#     #     return ['presence']

#     def connection_groups(self, **kwargs):
#         """Define the groups joined while connected"""
#         return ['presence-all']

#     def connect(self, message, **kwargs):
#         """Called when a WebSocket connection is opened."""
#         # TODO(raph): send connected users
#         message.reply_channel.send({
#             'text': json.dumps({
#                 'some_user_id1': 'some_user_data1',
#                 'some_user_id2': 'some_user_data2',
#             })
#         })

#         message.user.connected = True
#         message.user.save()

#         self.group_send('presence-all', {
#             message.user.id: 'user_data_of {}'.format(message.user.username)
#         })

#     def disconnect(self, message, **kwargs):
#         """Inform other users of the deconnection"""
#         message.user.connected = False
#         message.user.save()

#         self.group_send('presence-all', {
#             'module': 'presence',
#             'kind': 'disconnect',
#             'content': {
#                 message.user.id: self.get_user_data(message.user)
#             }
#         })

#     def receive(self, text=None, bytes=None, **kwargs):
#         print(text)

#     @classmethod
#     def get_user_data(cls, user):
#         return {
#             'username': user.username,
#             'connected': user.connected,
#         }
