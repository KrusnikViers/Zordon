import telegram as tg

from app.deprecated.utils import *


@callback_only
def on_abort(bot: tg.Bot, update: tg.Update):
    CallbackUtil.remove_message(bot, update)
