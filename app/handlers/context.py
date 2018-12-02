from telegram import Bot, Chat, Message, Update

from app.i18n.translations import Translations
from app.database.connection import DatabaseConnection
from app.database.scoped_session import ScopedSession
from app.database.util import get_with_update
from app.models.all import User, Group


class Context(ScopedSession):
    def __init__(self, update: Update, bot: Bot, db: DatabaseConnection, translations: Translations):
        super(Context, self).__init__(db)
        self.update = update
        self.bot = bot
        self.sender = self._maybe_get_user_from_update()
        self.users_joined, self.user_left = self._maybe_get_moved_users_from_update()
        self.group = self._maybe_get_group_from_update()
        self._translation = self._get_translation(translations)

    def send_response_message(self, text, **kwargs) -> Message:
        return self.update.effective_chat.send_message(text, **kwargs)

    def command_arguments(self) -> str:
        call_text = self.update.message.text
        divider_index = call_text.find(' ')
        if divider_index == -1:
            return ''
        return call_text[divider_index + 1:].strip()

    def __enter__(self):
        super(Context, self).__enter__()
        self._translation.install()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.update.callback_query:
            self.update.callback_query.answer()
        super(Context, self).__exit__(exc_type, exc_val, exc_tb)

    def _maybe_get_user_from_update(self) -> User:
        user = self.update.effective_user
        if not user:
            return None
        return get_with_update(self.session, User, user.id, login=user.username, name=user.full_name)

    def _maybe_get_group_from_update(self) -> Group:
        if self.update.effective_chat.type == Chat.PRIVATE:
            return None
        chat = self.update.effective_chat
        return get_with_update(self.session, Group, chat.id, name=chat.title)

    def _maybe_get_moved_users_from_update(self) -> (list, User):
        if not self.update.message:
            return [], None
        users_joined = []
        user_left = None
        if self.update.message.new_chat_members:
            users_joined = [
                get_with_update(self.session, User, tg_user.id, login=tg_user.username, name=tg_user.full_name)
                for tg_user in self.update.message.new_chat_members if not tg_user.is_bot]
        if self.update.message.left_chat_member:
            tg_user = self.update.message.left_chat_member
            user_left = get_with_update(self.session, User, tg_user.id, login=tg_user.username, name=tg_user.full_name)
        return users_joined, user_left

    def _get_translation(self, translations):
        if self.group and self.group.locale:
            return translations.get(self.group.locale)
        if self.sender and self.sender.locale:
            return translations.get(self.sender.locale)
        if self.update.effective_user:
            return translations.get(self.update.effective_user.language_code)
        return translations.get('')
