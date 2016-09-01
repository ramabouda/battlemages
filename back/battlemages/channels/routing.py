from channels import include, route_class
from .demultiplexer import Demultiplexer


channel_routing = [
    route_class(Demultiplexer, path=r'^/ws/$'),
    include("battlemages.channels.presence.routing.channel_routing"),
]
