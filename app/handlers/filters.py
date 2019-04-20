from telegram import Chat, Update

from app.handlers.util.inline_menu import callback_data


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

    # Let pass the message with no effective_chat, effective_user or message.
    NOT_FULL_DATA = 30

    _CHECKS = {
        GROUP: lambda x: x.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP],
        PRIVATE: lambda x: x.effective_chat.type == Chat.PRIVATE,
        CALLBACK: lambda x: x.callback_query is not None,
        PERSONAL_CALLBACK: _check_personal_callback,
    }

    _NO_CHECKS = {
        NOT_FULL_DATA
    }

    @staticmethod
    def _basic_filters(filters: list, update: Update):
        return update.effective_chat and \
               update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP, Chat.PRIVATE] and \
               not (update.effective_user and update.effective_user.is_bot) and \
               (Filter.NOT_FULL_DATA in filters or (update.effective_user and
                                                    update.effective_chat and
                                                    update.message))

    @staticmethod
    def apply(filters: list, update: Update):
        if not Filter._basic_filters(filters, update):
            return False
        for filter_value in filters:
            if not (filter_value in Filter._NO_CHECKS or Filter._CHECKS[filter_value](update)):
                return False
        return True
