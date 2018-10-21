COMMANDS_LIST = [
    'cancel',
    'call_join',
    'call_decline'
    'language_setup_menu',
    'language_setup_choose'
]

_command_codes = {name: index for index, name in enumerate(COMMANDS_LIST)}


def str_code(command: str) -> str:
    return str(_command_codes[command])

