from telegram import Chat, Update


class ChatType:
    INVALID = -1
    GROUP = 1
    PRIVATE = 2
    CALLBACK_GROUP = 3
    CALLBACK_PRIVATE = 4

    @staticmethod
    def _get_chat_type(update: Update) -> int:
        chat_type = ChatType.INVALID
        if update.effective_chat.type == Chat.PRIVATE:
            chat_type = ChatType.CALLBACK_PRIVATE if update.callback_query else ChatType.PRIVATE
        elif update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            chat_type = ChatType.CALLBACK_GROUP if update.callback_query else ChatType.GROUP
        return chat_type

    @classmethod
    def is_valid(cls, chat_filters: list, update: Update) -> bool:
        if update.effective_chat:
            return cls._get_chat_type(update) in chat_filters
        return False
