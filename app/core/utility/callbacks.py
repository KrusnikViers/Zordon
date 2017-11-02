from telegram import Update

from app.core import commands


def make_data(command, data: list) -> str:
    return ' '.join([str(commands.get(command).code)] + [str(x) for x in data])


def parse_data(update: Update) -> tuple:
    # First element is a command identifier
    return tuple(update.callback_query.data.split()[1:])
