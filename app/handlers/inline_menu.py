from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update

from app.handlers import commands


class InlineMenu(InlineKeyboardMarkup):
    # Expects a list of rows, where each row is a list of tuples ('Button text', [command_name, <parameters>])
    def __init__(self, markup: list, close_button_text: str = ''):
        if close_button_text:
            markup.append([(close_button_text, ['cancel'])])

        def encode(data): return ' '.join([commands.str_code(data[0])] + [str(x) for x in data[1:]])
        super(InlineMenu, self).__init__([[InlineKeyboardButton(text, callback_data=encode(data))
                                           for text, data in row] for row in markup])


def callback_data(update: Update) -> tuple:
    # First element is a command identifier.
    return tuple(update.callback_query.data.split()[1:])


def callback_pattern(command: str, has_parameters: bool) -> str:
    return '^{0}{1}$'.format(commands.str_code(command), '\ .+' if has_parameters else '')
