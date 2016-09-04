from channels.generic.websockets import BaseConsumer
from channels.generic.websockets import WebsocketDemultiplexer
from channels import Group


class DefaultGenericConsumerMixin(object):
    """
    Basic structure to plug actions on connection, disconnection
    """

    def raw_connect(self, message, **kwargs):
        """
        Called when a connection is opened. Base level so you don't
        need to call super() all the time.
        """
        self.connect(message, **kwargs)

    def connect(self, message, **kwargs):
        """
        Called when a connection is opened.
        """
        pass

    def close(self):
        """
        Closes the from the server end
        """
        self.message.reply_channel.send({"close": True})

    def raw_disconnect(self, message, **kwargs):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        self.disconnect(message, **kwargs)

    def disconnect(self, message, **kwargs):
        """
        Called when a WebSocket connection is opened.
        """
        pass

    def raw_receive(self, message, **kwargs):
        """
        Called when a WebSocket frame is received. Decodes it and passes it
        to receive().
        """
        self.receive(message, **kwargs)

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called with a decoded WebSocket frame.
        """
        pass


class GroupConsumerMixin(object):
    """
    A mixin to join groups at connection and leave them at disconnection
    """

    def connection_groups(self, **kwargs):
        """
        Group(s) to make people join when they connect and leave when they
        disconnect. Make sure to return a list/tuple, not a string!
        """
        return []

    def raw_connect(self, message, **kwargs):
        """
        Called when a WebSocket connection is opened. Base level so you don't
        need to call super() all the time.
        """
        for group in self.connection_groups(**kwargs):
            Group(group, channel_layer=message.channel_layer).add(message.reply_channel)
        super(GroupConsumerMixin, self).raw_connect(message, **kwargs)

    def raw_disconnect(self, message, **kwargs):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        for group in self.connection_groups(**kwargs):
            Group(group, channel_layer=message.channel_layer).discard(message.reply_channel)
        super(GroupConsumerMixin, self).raw_disconnect(message, **kwargs)


class MethodMappingCreator(type):

    def __new__(cls, name, bases, dct):
        """Generates the method mapping according to the consumer name

        Method mapping is used statically, it needs to be set at class creation
        """
        dct['method_mapping'] = {
            "{}.connect".format(dct['consumer_name']): "raw_connect",
            "{}.receive".format(dct['consumer_name']): "raw_receive",
            "{}.disconnect".format(dct['consumer_name']): "raw_disconnect",
        }
        return super(MethodMappingCreator, cls).__new__(cls, name, bases, dct)


class DemultiplexedConsumer(
    BaseConsumer,
    metaclass=MethodMappingCreator
):
    """
    A consumer class to receive messages from a multiplexed websocket
    """

    # The name used for the multiplexing.
    consumer_name = None

    def __init__(self, *args, **kwargs):
        """Ensures class config has been set."""
        if self.consumer_name is None:
            raise AttributeError('Attribute consumer_name must be defined.')
        super(DemultiplexedConsumer, self).__init__(*args, **kwargs)

    def raw_receive(self, message, **kwargs):
        """
        Called when a message is received from the demultiplexer. Decodes it and passes it
        to receive().
        """
        self.receive(message.content)

    def send(self, payload, close=False):
        """Send a serializable payload."""
        if close:
            payload["close"] = True
        message = self.format_message(payload)
        self.message.reply_channel.send(message)

    @classmethod
    def format_message(cls, payload):
        """Formats a serializable payload using the consumer name as the stream name"""
        return WebsocketDemultiplexer.encode(cls.consumer_name, payload)

    @classmethod
    def group_send(cls, name, payload, close=False):
        """Sends a formatted message to a group."""
        if close:
            payload["close"] = True
        message = cls.format_message(payload)
        Group(name).send(message)


class ConnectedDemultiplexedConsumer(
    GroupConsumerMixin,
    DemultiplexedConsumer,
    DefaultGenericConsumerMixin
):
    """
    Full featured consumer client for a demultiplexer, with groups and authentication
    """

    consumer_name = None
    channel_session_user = True
