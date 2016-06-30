from channels import Group


def connect_player(message):
    """Group with all the players"""
    Group('all-players').add(message.reply_channel)


def disconnect_player(message):
    Group('all-players').discard(message.reply_channel)
