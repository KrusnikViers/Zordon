from app.handlers.context import Context
from app.handlers import callback_utils


def on_menu_request(context: Context):
    if not context.group:
        message = _('user_setup_menu').format(context.sender.name)
        change_language_option = _('language_change_offer') if context.sender.locale else _('language_set_offer')
        menu = callback_utils.AttachedMenu([
            [(change_language_option, ['language_setup_menu'])]
        ])
        context.send_response_message(message, reply_markup=menu)
