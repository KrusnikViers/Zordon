from app.core.info import PROJECT_FULL_NAME
from app.handlers.context import Context
from app.models.all import User


def maybe_greet_user(context: Context, user: User, is_new_user: bool):
    # TODO: Should bot provide some help when it joins group?
    if context.group and context.group not in user.groups:
        user.groups.append(context.group)
        message_template = _('greet_{user}') if is_new_user else _('greet_known_{user}')
        context.send_response_message(message_template.format(user.name))


def farewell_left_user(context: Context):
    user: User = context.user_left[0]
    if context.group and context.group in user.groups:
        user.groups.remove(context.group)
        context.send_response_message(_('farevell_{user}').format(user.name))


def on_help_or_start(context: Context):
    message_template = _('{project}_help_for_group') if context.group else _('{project}_help_for_private')
    context.send_response_message(message_template.format(project=PROJECT_FULL_NAME))