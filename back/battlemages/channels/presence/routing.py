from channels import route

from .consumers import presence_consumer
from .consumers import connect_consumer


channel_routing = [
    route('presence.receive', presence_consumer),
    route('presence.connect', connect_consumer),
]
