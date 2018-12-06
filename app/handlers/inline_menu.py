from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from app.handlers import actions


class InlineMenu(InlineKeyboardMarkup):
    # Expects a list of rows, where each row is a list of tuples ('Button text', [command, <parameters>])
    def __init__(self, markup: list, close_button_text: str = ''):
        if close_button_text:
            markup.append([(close_button_text, [actions.Callback.CANCEL])])

        def encode(data): return ' '.join([str(x) for x in data])
        super(InlineMenu, self).__init__([[InlineKeyboardButton(text, callback_data=encode(data))
                                           for text, data in row] for row in markup])


def callback_data(update: Update) -> tuple:
    # First element is a command identifier.
    return tuple(update.callback_query.data.split()[1:])


def callback_pattern(command: int, has_parameters: bool) -> str:
    return '^{0}{1}$'.format(str(command), '\ .+' if has_parameters else '')
