from channels.generic.websockets import WebsocketDemultiplexer
from channels.channel import Channel

class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    mapping = {
        "presence": "presence.receive",
    }

    def connect(self, message, **kwargs):
        for k, v in self.mapping.items():
            Channel('{}.connect'.format(k)).send(message.content)

    def disconnect(self, message, **kwargs):
        for k, v in self.mapping.items():
            Channel('{}.disconnect'.format(k)).send(message.content)
