import telegram as tg

from app.handlers.utils import *
from app.models import *


@personal_command('u_status')
def on_status(bot: tg.Bot, update: tg.Update, user: User):
    response = "Current status: {0}".format("Active (receiving all notifications)"
                                            if user.is_active else
                                            "Do not disturb (summon notifications ignored)")
    if user.is_superuser():
        response += "\nSuperuser mode enabled. Use this power wisely."
    else:
        if user.rights_level > 0:
            response += "\nYou have right to manage activities and summon other people."
    return response, UserKeyboard(user)


@personal_command('u_activate')
def on_activate(bot: tg.Bot, update: tg.Update, user: User):
    if user.is_active:
        return "Active mode already enabled."

    if not user.is_active:
        suppressed_summons = (Activity.select()
                                      .join(Subscription).where(Subscription.user == user)
                                      .switch(Activity)
                                      .join(Participant).where(Participant.is_accepted == True)
                                      .group_by(Activity).having(pw.fn.Count(Participant.id) > 0))
        suppressed_summons = pw.prefetch(suppressed_summons, (Participant.select(Participant, User)
                                                                         .where(Participant.is_accepted == True)
                                                                         .join(User)))
        for activity in suppressed_summons:
            user.send_message(bot,
                              text='There is active {0} session!\n'
                                   'Already joined: {1}\n'
                                   'Want to join too?'.format(
                                        activity.name_md(),
                                        ', '.join([p.user.telegram_login for p in activity.participant_set_prefetch])),
                              reply_markup=ResponseInlineKeyboard(activity.name))
    user.is_active = True
    user.save()
    return "Status updated to Active", UserKeyboard(user)


@personal_command('u_deactivate')
def on_deactivate(bot: tg.Bot, update: tg.Update, user: User):
    if not user.is_active:
        return "Do not disturb mode already enabled."

    if user.is_active:
        user_activities = Activity.select().join(Participant).where(Participant.user == user)
        other_participants = (User.select().where(User.telegram_user_id != user.telegram_user_id)
                                  .join(Participant).where((Participant.activity.in_(user_activities)) &
                                                           (Participant.is_accepted == True))
                                  .group_by(User))
        for fellow_participant in other_participants:
            fellow_participant.send_message(bot,
                                            text='{0} became inactive and leaved all sessions.'.format(
                                                user.telegram_login))
        Participant.delete().where(Participant.user == user).execute()
    user.is_active = False
    user.save()
    return "Status updated to Do not disturb", UserKeyboard(user)


@personal_command('u_cancel')
def on_cancel(bot: Bot, update: Update, user: User):
    if user.pending_action == pending_user_actions['none']:
        return 'Nothing to be cancelled.', UserKeyboard(user)

    cancelled_action = user.pending_action
    user.pending_action = pending_user_actions['none']
    user.save()
    cancel_replies = {
        pending_user_actions['a_new']: 'New activity adding cancelled.',
        pending_user_actions['u_report']: 'Reporting cancelled',
    }
    return cancel_replies[cancelled_action], UserKeyboard(user)


@personal_command('u_report')
def on_report(bot: Bot, update: Update, user: User):
    if user.pending_action not in {pending_user_actions['none'], pending_user_actions['u_report']}:
        on_cancel(bot, update, user)

    user.pending_action = pending_user_actions['u_report']
    user.save()
    return 'Send me message to report (text only):', UserKeyboard(user)


@personal_command('u_report')
def on_report_with_data(bot: Bot, update: Update, user: User):
    user.pending_action = pending_user_actions['none']
    user.save()
    User.send_message_to_superuser(bot, text=update.message.text)
    return 'Your message had been sent to superuser', UserKeyboard(user)
