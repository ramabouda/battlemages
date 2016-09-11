from battlemages.channels.lib import WebsocketConsumerDemultiplexer
from .presence.consumers import PresenceConsumer


class Demultiplexer(WebsocketConsumerDemultiplexer):
    http_user = True
    slight_ordering = True

    consumers = [
        PresenceConsumer,
    ]
