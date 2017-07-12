import telegram as tg

from .common import *
from ..models import *


@personal_command('status')
def on_status(bot: tg.Bot, update: tg.Update, user: User):
    response = "Current status: {0}".format("*Active* (receiving all notifications)"
                                            if user.is_active else
                                            "*Do not disturb* (summon notifications ignored)")
    if update.effective_user.name == superuser_login:
        response += "\nSuperuser mode enabled. Use this power wisely."
    elif user.is_moderator:
        response += "\nEnabled rights to manage activities and summon other people."
    return response, build_default_keyboard(user)


@personal_command('activate')
def on_activate(bot: tg.Bot, update: tg.Update, user: User):
    if user.is_active:
        return "*Active* mode already enabled."

    if not user.is_active:
        suppressed_summons = (Activity.select().join(Subscription).where(Subscription.user == user).switch(Activity)
                                               .join(Participant).aggregate_rows())
        for activity in suppressed_summons:
            user.send_message(bot,
                              text='Summon is active for *{0}*'.format(activity.name),
                              reply_markup=build_summon_response_keyboard(activity.name))
    user.is_active = True
    user.save()
    return "Status updated to *Active*", build_default_keyboard(user)


@personal_command('deactivate')
def on_deactivate(bot: tg.Bot, update: tg.Update, user: User):
    if not user.is_active:
        return "*Do not disturb* mode already enabled."

    if user.is_active:
        Participant.delete().where(Participant.user == user).execute()
    user.is_active = False
    user.save()
    return "Status updated to *Do not disturb*", build_default_keyboard(user)


@personal_command('cancel')
def on_cancel(bot: Bot, update: Update, user: User):
    if user.pending_action == pending_user_actions['none']:
        return 'Nothing to be cancelled.', build_default_keyboard(user)

    cancelled_action = user.pending_action
    user.pending_action = pending_user_actions['none']
    user.save()
    if cancelled_action == pending_user_actions['activity_add']:
        return 'New activity adding cancelled.', build_default_keyboard(user)


@personal_command('raw_data')
def on_raw_data(bot: Bot, update: Update, user: User):
    users = User.select()
    response = "User list:"
    for raw_user in users:
        response += "\n{0} : rights {1}, pending {2}, active: {3}, disabled: {4}".format(
            raw_user.telegram_login, raw_user.rights_level, raw_user.pending_action, raw_user.is_active,
            raw_user.is_disabled_chat)
    user.send_message(bot, text=response)

    activities = Activity.select(Activity, User).join(User)
    response = "Activities list:"
    for activity in activities:
        response += "\n*{0}* - owner {1}".format(activity.name, activity.owner.telegram_login)
    user.send_message(bot, text=response)

    subscriptions = Subscription.select(Activity, Subscription, User).join(Activity).join(User)
    response = "Subscriptions:"
    for subscription in subscriptions:
        response += "\n{0} to {1}".format(subscription.user.telegram_login, subscription.activity.name)
    user.send_message(bot, text=response)

    Participant.clear_inactive()
    participants = Participant.select(Activity, Participant, User).join(Activity).join(User)
    response = "Participants:"
    for participant in participants:
        response += "\n{0} in {1} ({2} from {3})".format(participant.user.telegram_login, participant.activity.name,
                                                         participant.is_accepted, participant.report_time)
    user.send_message(bot, text=response)
