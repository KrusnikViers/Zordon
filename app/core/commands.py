# Add new commands in this list. Sections are divided by rights level required, commands inside section should be sorted
# in alphabetic order. Related variables are being built from the |_commands_by_rights_level|.
_commands_by_rights_level = [
    # Commands, available for just-joined user.
    [
        'activity_accessed',
        'activity_menu',
        'activity_public',
        'activity_subscriptions',
        'subscription_accept_call',
        'subscription_accept_call_later',
        'subscription_accept_call_later_time',
        'subscription_decline_call',
        'subscription_delete',
        'subscription_new',
        'subscription_reply_with_message',
        'system_cancel',
        'system_close_menu',
        'system_help',
        'system_report',
        'user_menu',
        'user_show_rights_description',
        'user_switch_keyboard_layout',
        'user_switch_status',
    ],
    # Commands, available for user, approved as trusted.
    [
        'activity_delete',
        'activity_new',
        'subscription_call',
    ],
    # Superuser commands (this section must ALWAYS go last).
    [
        'system_full_information',
        'user_demote',
        'user_promote',
    ],
]

superuser_rights_level = len(_commands_by_rights_level) - 1


class Command:
    def __init__(self, name: str, code: int, rights_level: int):
        self.name = name
        self.code = code
        self.rights_level = rights_level

    by_code = {}  # command.code: Command
    by_name = {}  # command.name: Command


def get(identifier) -> Command:
    """ Returns Command object, determining if identifier is string/integer and searching by name/code """
    if isinstance(identifier, Command):
        return identifier
    elif isinstance(identifier, str):
        return Command.by_name[identifier]
    elif isinstance(identifier, int):
        return Command.by_code[identifier]
    # Should not reach this place.
    assert False

# Implementation.
#################

# Form |Command| object for all commands in list.
_all_commands = []
_code_counter = 0
for rights_level in range(0, len(_commands_by_rights_level)):
    for command_name in _commands_by_rights_level[rights_level]:
        _all_commands.append(Command(command_name, _code_counter, rights_level))
        _code_counter += 1

# Form result dictionaries that will be used by bot.
for command in _all_commands:
    assert command.name not in Command.by_name
    Command.by_name[command.name] = command
    assert command.code not in Command.by_code
    Command.by_code[command.code] = command

# After this was executed, variables below must not be used any more.
del _commands_by_rights_level
del _all_commands
del _code_counter
