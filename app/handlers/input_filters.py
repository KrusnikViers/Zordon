from telegram import Chat, Update

from app.handlers.inline_menu import callback_data


def _check_personal_callback(update: Update):
    if update.callback_query is None or not update.effective_user:
        return False
    data = callback_data(update)
    return len(data) > 0 and int(data[0]) == update.effective_user.id


class Filter:
    # Messages from groups and supergroups.
    GROUP = 1
    # Messages only from private chats.
    PRIVATE = 2
    # Check, that message is a callback from inline menu button.
    CALLBACK = 10
    # Same as previous, but also checks that first argument of the callback data is equal to sender's id.
    PERSONAL_CALLBACK = 11
    # Ensures, that message has effective_chat, effective_user and message.
    FULL_DATA = 30

    _CHECKS = {
        GROUP: lambda x: x.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP],
        PRIVATE: lambda x: x.effective_chat.type == Chat.PRIVATE,
        CALLBACK: lambda x: x.callback_query is not None,
        PERSONAL_CALLBACK: _check_personal_callback,
        FULL_DATA: lambda x: x.effective_user and x.effective_chat and x.message,
    }

    @staticmethod
    def _basic_filters(update: Update):
        return update.effective_chat and \
               update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP, Chat.PRIVATE] and \
               not (update.effective_user and update.effective_user.is_bot)

    @staticmethod
    def apply(filters: list, update: Update):
        if not Filter._basic_filters(update):
            return False
        for filter_value in filters:
            if not Filter._CHECKS[filter_value](update):
                return False
        return True
