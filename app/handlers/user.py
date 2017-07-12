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
        Participant.delete().where(Participant.user == user)
    user.is_active = False
    user.save()
    return "Status updated to *Do not disturb*", build_default_keyboard(user)


@personal_command()
def on_cancel(bot: Bot, update: Update, user: User):
    if user.pending_action == pending_user_actions['none']:
        return 'Nothing to be cancelled.'

    cancelled_action = user.pending_action
    user.pending_action = pending_user_actions['none']
    user.save()
    if cancelled_action == pending_user_actions['activity_add']:
        return 'New activity adding cancelled.'
