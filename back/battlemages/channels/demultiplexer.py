from channels.generic.websockets import WebsocketDemultiplexer
from channels.channel import Channel

class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    mapping = {
        "presence": "presence.receive",
    }

    def connect(self, message, **kwargs):
        Channel('presence.connect').send(message.content)
