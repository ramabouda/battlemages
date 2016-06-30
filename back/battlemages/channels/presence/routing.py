from channels import route

import consumers


# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. WebSocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# While this is under stream/ compared to the HTML page, we could have it on the
# same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
channel_routing = [
    # Called when incoming WebSockets connect
    route("websocket.connect", consumers.connect_player, path=r'^/ws/$'),

    # Called when the client closes the socket
    route("websocket.disconnect", consumers.disconnect_player, path=r'^/ws/$'),
]
