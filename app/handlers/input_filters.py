from telegram import Chat, Update


INVALID = -1
ALL = 0


class ChatFilter:
    GROUP = 1
    PRIVATE = 2

    @classmethod
    def from_update(cls, update: Update):
        if update.effective_chat.type == Chat.PRIVATE:
            return cls.PRIVATE
        elif update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            return cls.GROUP
        return INVALID


class MessageFilter:
    CALLBACK = 1

    @classmethod
    def from_update(cls, update: Update):
        if update.callback_query:
            return cls.CALLBACK
        return INVALID


class InputFilters:
    def __init__(self, chat=ALL, message=ALL):
        self.chat = chat
        self.message = message


def is_message_valid(input_filters: InputFilters, update: Update) -> bool:
    return update.effective_chat and \
           input_filters.chat in [ALL, ChatFilter.from_update(update)] and \
           input_filters.message in [ALL, MessageFilter.from_update(update)]
