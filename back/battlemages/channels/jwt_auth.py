from functools import wraps
from json import loads, dumps

from channels.handler import AsgiRequest
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


def _close_reply_channel(message):
    message.reply_channel.send({'close': True})


class DirectJwtAuthentication(BaseJSONWebTokenAuthentication):
    """
    Authenticates directly based on the token
    """

    def get_jwt_value(self, token):
        """Used by the parent class"""
        return token


def jwt_request_user(func):
    """
    Check the presence of a "token" request parameter and tries to
    authenticate the user based on its content.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):
        # Taken from channels.session.http_session
        try:
            if "method" not in message.content:
                message.content['method'] = "FAKE"
            request = AsgiRequest(message)
        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)

        token = request.GET.get("token", None)
        if token is None:
            _close_reply_channel(message)
            raise ValueError("Missing token request parameter. Closing channel. Message: {}".format(message.content))

        user = DirectJwtAuthentication().authenticate(token)[0]

        message.token = token
        message.user = user

        return func(message, *args, **kwargs)
    return inner


def jwt_message_user(func):
    """
    Check the presence of a "token" field on the message's text field and
    tries to authenticate the user based on its content.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):
        message_text = message.get('text', None)
        if message_text is None:
            _close_reply_channel(message)
            raise ValueError("Missing text field. Closing channel.")

        try:
            message_text_json = loads(message_text)
        except ValueError:
            _close_reply_channel(message)
            raise

        token = message_text_json.pop('token', None)
        if token is None:
            _close_reply_channel(message)
            raise ValueError("Missing token field. Closing channel.")

        user = DirectJwtAuthentication().authenticate(token)[0]

        message.token = token
        message.user = user
        message.text = dumps(message_text_json)

        return func(message, *args, **kwargs)
    return inner
