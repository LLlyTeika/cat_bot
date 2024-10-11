import logging


def take_message(username):
    logging.info(f"сообщение от пользователя: {username}")


def new_user(username, user_id):
    logging.info(f"новый пользователь: {username}, id: {user_id}")