import telegram as tg

from ..models import *
from .utils import *


@personal_command('p_summon')
def on_summon(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select(Activity.name).join(Subscription).where(Subscription.user == user)
    if not activities.exists():
        return 'Activities list is empty.'

    return 'Select activity for summon:', KeyboardBuild.inline([[(x.name, 'p_summon ' + x.name)] for x in activities],
                                                               'Close selection')


@callback_only
@personal_command('p_summon')
def on_summon_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        CallbackUtil.edit(update, error)
        return

    Participant.response_to_summon(bot, user, activity, 'p_summon')
    inactive_users = Participant.select_subscribers_for_activity(activity)
    for inactive_user in Participant.select_subscribers_for_activity(activity):
        inactive_user.send_message(bot,
                                   text='{0} is summoning you for {1}!'.format(user.telegram_login, activity.name_md()),
                                   reply_markup=KeyboardBuild.summon_response(activity.name))

    participants = Participant.select_participants_for_activity(activity, user)
    if participants:
        user.send_message(bot, text='Already joined: ' + ', '.join([p.telegram_login for p in participants]))

    if not inactive_users:
        return 'There are no more users to be invited.'
    return 'Invitations to {0} was sent to: {1}'.format(activity.name_md(),
                                                        ', '.join([x.telegram_login for x in inactive_users]))


@callback_only
@personal_command('p_accept')
def on_accept_now_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        CallbackUtil.edit(update, error)
        return

    Participant.response_to_summon(bot, user, activity, 'p_accept')
    CallbackUtil.edit(update, 'Invitation to {0} accepted!'.format(activity.name_md()),
                      KeyboardBuild.summon_response(activity.name, True))
    participants = Participant.select_participants_for_activity(activity, user)
    if participants:
        return 'Other joined: ' + ', '.join([p.telegram_login for p in participants])


@callback_only
@personal_command('p_accept_later')
def on_accept_later_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        CallbackUtil.edit(update, error)
        return

    Participant.response_to_summon(bot, user, activity, 'p_accept_later')
    CallbackUtil.edit(update, 'Invitation to {0} accepted!'.format(activity.name_md()),
                      KeyboardBuild.summon_response(activity.name, True))
    participants = Participant.select_participants_for_activity(activity, user)
    if participants:
        return 'Other joined: ' + ', '.join([p.telegram_login for p in participants])


@callback_only
@personal_command('p_decline')
def on_decline_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        CallbackUtil.edit(update, error)
        return

    Participant.response_to_summon(bot, user, activity, 'p_decline')
    CallbackUtil.edit(update, 'Invitation to {0} declined. Next time then!'.format(activity.name_md()),
                      KeyboardBuild.summon_response(activity.name, False))
