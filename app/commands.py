import telegram.ext
from models import *
from utils import personal_command


@personal_command
def _on_start(bot, update, _):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome! Let's fight evil and boredom together, friend.")


@personal_command
def _on_status(bot, update, user):
    response = "{0}, at the moment you are {1}{2}."\
        .format(update.effective_user.name,
                "ready for invitations" if user.is_active else "not receiving invitations",
                " and able to summon people or create activities" if user.is_moderator else "")
    bot.send_message(chat_id=update.message.chat_id, text=response)


def set_handlers(dispatcher):
    dispatcher.add_handler(telegram.ext.CommandHandler('start', _on_start))
    dispatcher.add_handler(telegram.ext.CommandHandler('status', _on_status))
