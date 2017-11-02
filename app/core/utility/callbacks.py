from telegram import Update

from app.core import commands


def make_data(command, data: list) -> str:
    return ' '.join([str(commands.get(command).code)] + [str(x) for x in data])


def parse_data(update: Update) -> tuple:
    # First element is a command identifier
    return tuple(update.callback_query.data.split()[1:])


def make_pattern(command, has_data: bool = False) -> str:
    return '^{0}{1}$'.format(str(commands.get(command).code), '\ .+' if has_data else '')
