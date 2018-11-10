from telegram import Chat, Update


class ChatType:
    GROUP = 1
    PRIVATE = 2
    CALLBACK_GROUP = 3
    CALLBACK_PRIVATE = 4

    @staticmethod
    def is_valid(chat_filters: list, update: Update) -> bool:
        if not update.effective_chat:
            return False
        if update.effective_chat.type == Chat.PRIVATE:
            if update.callback_query:
                return ChatType.CALLBACK_PRIVATE in chat_filters
            else:
                return ChatType.PRIVATE in chat_filters
        elif update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            if update.callback_query:
                return ChatType.CALLBACK_GROUP in chat_filters
            else:
                return ChatType.GROUP in chat_filters
