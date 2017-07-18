import telegram as tg

import app.handlers.user as u
from ..models import *
from .utils import *


def _build_list_keyboard(user: User, available_actions: set)->tg.InlineKeyboardMarkup:
    activity_list_full_keyboard = [
        [('p_summon', 'Summon friends')],
        [('s_new', 'Subscribe...'), ('s_delete', 'Unsubscribe...')],
        [('a_new', 'Create new...'), ('a_delete', 'Delete...')]
    ]
    keyboard = [
        [(name, command) for command, name in row
         if (command in available_actions) and user.has_right_to(command)]
        for row in activity_list_full_keyboard
    ]
    return KeyboardBuild.inline(keyboard)


@personal_command('a_list')
def on_list(bot: tg.Bot, update: tg.Update, user: User):
    available_actions = {'a_new'}
    if not Activity.select().exists():
        return 'Activities list is empty.', _build_list_keyboard(user, available_actions)

    user_activities = Activity.select().join(Subscription).where(Subscription.user == user)
    other_activities_count = Activity.select(Activity.name).where(Activity.id.not_in(user_activities)).count()

    if not user_activities:
        response = 'Subscriptions list is empty.'
    else:
        Participant.clear_inactive()
        user_activities = pw.prefetch(user_activities, Participant.select().join(User))
        not_responded_subscribers = (Subscription.select().join(User).where((User.is_active == True) &
                                                                            (User.is_disabled_chat == False))
                                                          .switch(Subscription)
                                                          .join(Participant,
                                                                pw.JOIN_LEFT_OUTER,
                                                                on=((Participant.activity == Subscription.activity) &
                                                                    (Participant.user == Subscription.user)))
                                                          .where(Participant.id.is_null()))
        user_activities = pw.prefetch(user_activities, not_responded_subscribers)

        available_actions = available_actions.union({'p_summon', 's_delete'})
        activity_records = []
        for activity in user_activities:
            record = '{0}'.format(activity.name_md())
            if activity.has_right_to_remove(user):
                record += '\n owned by you'
                available_actions.add('a_delete')
            if activity.participant_set_prefetch:
                online_users = [participant.user.telegram_login for participant in activity.participant_set_prefetch]
                record += '\n joined now: ' + ', '.join(online_users)
                record += '\n have not responded: *{0}*'.format(len(activity.subscription_set_prefetch))
            else:
                record += '\n active subscribers: *{0}*'.format(len(activity.subscription_set_prefetch))
            activity_records.append(record)
        response = '\n\n'.join(activity_records)

    if other_activities_count:
        response += '\n\n*{0}* more activities available to subscribe.'.format(other_activities_count)
        available_actions.add('s_new')

    return response, _build_list_keyboard(user, available_actions)


@personal_command('a_new')
def on_new(bot: tg.Bot, update: tg.Update, user: User):
    if user.pending_action not in {pending_user_actions['none'], pending_user_actions['a_new']}:
        u.on_cancel(bot, update, user)
    user.pending_action = pending_user_actions['a_new']
    user.save()
    return 'Send me name for activity to create:', KeyboardBuild.default(user)


@personal_command('a_new')
def on_new_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error_message = Activity.try_to_create(update.message.text, user)
    if not activity:
        return 'Try another name: ' + error_message

    Subscription.create(user=user, activity=activity)
    user.pending_action = pending_user_actions['none']
    user.save()
    User.send_message_to_superuser(bot, text='{0} created activity {1}'.format(user.telegram_login, activity.name_md()))
    return 'Activity {0} created!'.format(activity.name_md()), KeyboardBuild.default(user)


@personal_command('a_delete')
def on_delete(bot: tg.Bot, update: tg.Update, user: User):
    return _on_delete_impl(bot, update, user)


def _on_delete_impl(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select().order_by(Activity.name)
    if not user.is_superuser():
        activities = activities.where(Activity.owner == user)
    if not activities.exists():
        return 'There are no activities you can remove.'

    return ('Select activity to remove:',
            KeyboardBuild.inline([[(x.name, 'a_delete ' + x.name)] for x in activities], 'Close selection'))


@callback_only
@personal_command('a_delete')
def on_delete_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity_name = CallbackUtil.get_data(update.callback_query.data)
    activity, error = Activity.try_to_get(activity_name)
    if not activity:
        CallbackUtil.edit(update, error)
        return

    if not activity.has_right_to_remove(user):
        CallbackUtil.edit(update, 'You have not enough rights to remove {0}.'.format(activity.name_md()))
        return

    activity.delete_instance()
    CallbackUtil.edit(update, _on_delete_impl(bot, update, user))
    return 'Activity {0} successfully deleted!'.format(activity.name_md())
