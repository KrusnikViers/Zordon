import models


def personal_command(decorated_handler):
    def wrapper(bot, update):
        if not update.effective_user:
            return
        user = models.User.get_or_create(telegram_id=update.effective_user.id,
                                         defaults={'is_active': True, 'is_moderator': False})[0]
        decorated_handler(bot, update, user)
    return wrapper
