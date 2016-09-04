from channels import route, route_class

from .consumers import PresenceConsumer


channel_routing = [
    route_class(PresenceConsumer)
]
