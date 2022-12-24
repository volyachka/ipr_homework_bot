def handle_username(message):
    username = message.from_user.username
    return username if username is not None else " "