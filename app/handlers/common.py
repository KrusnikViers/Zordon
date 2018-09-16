from app.handlers.context import Context


def maybe_greet_user(context: Context):
    if context.group and context.group not in context.sender.groups:
        context.sender.groups.append(context.group)
        message_template = _('greet_{user}_in_group') if context.is_new_user else _('greet_known_{user}_in_group')
        context.send_message(message_template.format(context.sender.name))


def on_help_or_start(context: Context):
    context.send_message(_('help_for_group') if context.group else _('help_for_private'))
