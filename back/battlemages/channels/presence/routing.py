from channels import route_class

from .consumers import PresenceConsumer


channel_routing = [
    route_class(PresenceConsumer)
]
