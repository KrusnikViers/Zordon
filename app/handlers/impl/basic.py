from app.core.info import PROJECT_FULL_NAME
from app.handlers.context import Context


def on_help_or_start(context: Context):
    message_template = _('{project}_help_for_group') if context.group else _('{project}_help_for_private')
    context.send_response_message(message_template.format(project=PROJECT_FULL_NAME))


def on_click_here(context: Context):
    context.send_response_message(_('rdr2_easter_egg'))