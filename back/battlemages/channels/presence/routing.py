from channels import route_class

from .consumers import PresenceConsumer


# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. WebSocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# While this is under stream/ compared to the HTML page, we could have it on the
# same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
channel_routing = [
    route_class(PresenceConsumer, path=r'^/ws/$'),
]
