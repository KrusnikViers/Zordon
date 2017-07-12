import telegram as tg

from ..models import *
from .common import *


@personal_command('summon')
def on_summon(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select()
    if not activities.exists():
        return 'No activities available'
    return 'Select activity for summon:', build_inline_keyboard([[(x.name, 'summon ' + x.name)] for x in activities])


@callback_only
@personal_command('summon')
def on_summon_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.get_from_callback_data(update.callback_query.data)
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'join')
    for inactive_user in Participant.select_inactive_users(activity):
        inactive_user.send_message(bot,
                                   text='{0} is summoning you for *{1}*'.format(user.telegram_login, activity.name),
                                   reply_markup=build_inline_keyboard([[('Join now', 'join ' + activity.name),
                                                                        ('Coming', 'later ' + activity.name),
                                                                        ('Decline', 'decline ' + activity.name)]]))


@callback_only
@personal_command('join')
def on_join_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.get_from_callback_data(update.callback_query.data)
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'join')


@callback_only
@personal_command('later')
def on_later_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.get_from_callback_data(update.callback_query.data)
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'later')


@callback_only
@personal_command('decline')
def on_decline_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.get_from_callback_data(update.callback_query.data)
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'decline')
