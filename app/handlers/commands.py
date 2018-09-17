command_list = [
    'cancel',
    'language_setup_menu',
    'language_setup_choose'
]

_command_codes = {name: index for index, name in enumerate(command_list)}


def str_code(command: str) -> str:
    return str(_command_codes[command])
