COMMANDS_LIST = [
    'cancel',
    'recall_join',
    'recall_decline'
]

_command_codes = {name: index for index, name in enumerate(COMMANDS_LIST)}


def str_code(command: str) -> str:
    return str(_command_codes[command])
