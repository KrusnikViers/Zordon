from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, CommandHandler

from app.core import commands
from app.core.utility import callbacks, keyboard, wrappers
from app.models.all import *


@wrappers.personal_command('user_menu')
def menu(bot: Bot, update: Update, user: User):
    rights = ([
        _('user_menu_rights_desc_0'),
        _('user_menu_rights_desc_1'),
        _('user_menu_rights_desc_2'),
    ])[user.rights]
    status = ([
        'disabled',
        _('user_menu_status_desc_active'),
        _('user_menu_status_desc_do_not_disturb')
    ])[user.status]

    text = _('user_menu_text {login} {rights}').format(login=user.login, rights=rights)
    lang_auto_mark = '' if user.locale != 'auto' else _('user_menu_kb_lang_auto_mark')
    markup = keyboard.InlineKeyboard([
        [(_('user_menu_kb_status {status}').format(status=status), commands.str_code('user_switch_status'))],
        [
            (_('user_menu_kb_lang {lang} {auto}').format(lang=_('system_lang_name'), auto=lang_auto_mark),
             commands.str_code('user_change_language'))
        ],
    ], _('system_close'))
    # In most cases, this will cause new message to be sent.
    callbacks.maybe_update(bot, update, user, text, markup)


@wrappers.personal_command('user_switch_status')
def switch_status(bot: Bot, update: Update, user: User):
    if user.status != user.statuses['active']:
        user.status = user.statuses['active']
    else:
        user.status = user.statuses['do_not_disturb']
    user.save()
    menu(bot, update, user)


@wrappers.personal_command('user_change_language')
def change_language(bot: Bot, update: Update, user: User):
    text = update.callback_query.message.text
    markup = keyboard.InlineKeyboard([
        [(_('user_change_language_kb_auto'), callbacks.make_data('user_change_language', ['auto']))],
        [(_('user_change_language_kb_en'), callbacks.make_data('user_change_language', ['en']))],
        [(_('user_change_language_kb_ru'), callbacks.make_data('user_change_language', ['ru']))],
    ], _('system_close'))
    callbacks.maybe_update(bot, update, user, text, markup)


@wrappers.personal_command('user_change_language')
def change_language_response(bot: Bot, update: Update, user: User):
    lang_code, = callbacks.parse_data(update)
    assert lang_code in {'auto', 'en', 'ru'}
    user.locale = lang_code
    user.save()
    menu(bot, update, user)


def get_handlers() -> list:
    return [
        CommandHandler('start', menu),
        CallbackQueryHandler(switch_status, pattern=callbacks.make_handler_pattern('user_switch_status')),
        CallbackQueryHandler(change_language, pattern=callbacks.make_handler_pattern('user_change_language')),
        CallbackQueryHandler(change_language_response,
                             pattern=callbacks.make_handler_pattern('user_change_language', has_data=True)),
    ]
