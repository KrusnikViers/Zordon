from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from .handlers.messages import message_handler

import app.handlers.activity as a
import app.handlers.participant as p
import app.handlers.subscription as s
import app.handlers.superuser as su
import app.handlers.user as u



def set_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', u.on_status))
    dispatcher.add_handler(CallbackQueryHandler(u.on_cancel, pattern="^u_cancel$"))
    dispatcher.add_handler(CommandHandler('report', u.on_report))

    dispatcher.add_handler(CallbackQueryHandler(a.on_new, pattern="^a_new$"))
    dispatcher.add_handler(CallbackQueryHandler(a.on_delete, pattern="^a_delete$"))
    dispatcher.add_handler(CallbackQueryHandler(a.on_delete_with_data, pattern="^a_delete\ .+$"))

    dispatcher.add_handler(CallbackQueryHandler(s.on_new, pattern="^s_new$"))
    dispatcher.add_handler(CallbackQueryHandler(s.on_new_with_data, pattern="^s_new\ .+$"))
    dispatcher.add_handler(CallbackQueryHandler(s.on_delete, pattern="^s_delete$"))
    dispatcher.add_handler(CallbackQueryHandler(s.on_delete_with_data, pattern="^s_delete\ .+$"))

    dispatcher.add_handler(CallbackQueryHandler(p.on_summon, pattern="^p_summon$"))
    dispatcher.add_handler(CallbackQueryHandler(p.on_summon_with_data, pattern="^p_summon\ .+$"))
    dispatcher.add_handler(CallbackQueryHandler(p.on_accept_now_with_data, pattern="^p_accept\ .+$"))
    dispatcher.add_handler(CallbackQueryHandler(p.on_accept_later_with_data, pattern="^p_accept_later\ .+$"))
    dispatcher.add_handler(CallbackQueryHandler(p.on_decline_with_data, pattern="^p_decline\ .+$"))

    dispatcher.add_handler(CallbackQueryHandler(su.on_promote, pattern="^su_promote$"))
    dispatcher.add_handler(CallbackQueryHandler(su.on_promote_with_data, pattern="^su_promote\ .+$"))
    dispatcher.add_handler(CallbackQueryHandler(su.on_demote, pattern="^su_demote$"))
    dispatcher.add_handler(CallbackQueryHandler(su.on_demote_with_data, pattern="^su_demote\ .+$"))

    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
