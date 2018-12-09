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
        return ALL


class InputFilters:
    def __init__(self, chat=ALL, message=ALL):
        self.chat = chat
        self.message = message


def _is_type_valid(filter_class, filter_value, update: Update):
    message_type = filter_class.from_update(update)
    return message_type != INVALID and (filter_value == ALL or filter_value == message_type)


def is_message_valid(input_filters: InputFilters, update: Update) -> bool:
    return update.effective_chat and \
           _is_type_valid(ChatFilter, input_filters.chat, update) and \
           _is_type_valid(MessageFilter, input_filters.message, update)
