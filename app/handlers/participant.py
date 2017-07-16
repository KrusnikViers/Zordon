import telegram as tg

from ..models import *
from .utils import *


@personal_command('p_summon')
def on_summon(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select(Activity.name).join(Subscription).where(Subscription.user == user)
    if not activities.exists():
        return 'No activities available'
    return 'Select activity for summon:', build_inline_keyboard([[(x.name, 'p_summon ' + x.name)] for x in activities])


@callback_only
@personal_command('p_summon')
def on_summon_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'p_summon')
    inactive_users = Participant.select_subscribers_for_activity(activity)
    if not inactive_users:
        return 'There are no users to answer your call'
    for inactive_user in Participant.select_subscribers_for_activity(activity):
        inactive_user.send_message(bot,
                                   text='{0} is summoning you for {1}'.format(user.telegram_login, activity.name_md()),
                                   reply_markup=build_summon_response_keyboard(activity.name))
    return 'Invitations to {0} was sent to {1}'.format(activity.name_md(),
                                                       ', '.join([x.telegram_login for x in inactive_users]))


@callback_only
@personal_command('p_accept')
def on_accept_now_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Responding...')
    if not activity:
        return error

    Participant.response_to_summon(bot, user, activity, 'p_accept')
    edit_callback_message(update,
                          'You have accepted the invitation to {0}'.format(activity.name_md()),
                          build_summon_response_keyboard(activity.name, True))


@callback_only
@personal_command('p_accept_later')
def on_accept_later_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Responding...')
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'p_accept_later')
    edit_callback_message(update,
                          'You have accepted the invitation to {0}'.format(activity.name_md()),
                          build_summon_response_keyboard(activity.name, True))


@callback_only
@personal_command('p_decline')
def on_decline_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Responding...')
    if not activity:
        return error
    Participant.response_to_summon(bot, user, activity, 'p_decline')
    edit_callback_message(update,
                          'You have declined the invitation to {0}'.format(activity.name_md()),
                          build_summon_response_keyboard(activity.name, False))
