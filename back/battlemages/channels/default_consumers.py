from battlemages.channels.lib import DemultiplexedConsumer
from battlemages.channels.lib import GroupConsumerMixin

class AuthenticatedGroupConsumer(GroupConsumerMixin, DemultiplexedConsumer):
    """
    Full featured consumer client for a demultiplexer, with groups and authentication
    """

    channel_session_user = True
    http_user = True
    stream_name = None
