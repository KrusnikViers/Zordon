import telegram as tg
import peewee as pw

from .utils import *
from ..models import *
import app.handlers.user as u


def _build_list_keyboard(available_actions: set)->tg.InlineKeyboardMarkup:
    buttons = [
        ('a_new', 'Create new',),
        ('a_delete', 'Delete existing',),
        ('s_new', 'Subscribe',),
        ('s_delete', 'Unsubscribe',),
        ('p_summon', 'Summon friends'),
    ]
    return build_inline_keyboard([[(name, command)] for command, name in buttons if command in available_actions])


@personal_command('a_list')
def on_list(bot: tg.Bot, update: tg.Update, user: User):
    available_actions = set()
    if user.has_right_to('a_new'):
        available_actions.add('a_new')

    # Selecting activities
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription, pw.JOIN_LEFT_OUTER)
                  .where((Subscription.id.is_null(True)) | (Subscription.user == user))
                  .order_by(Activity.name))
    if not activities.exists():
        return 'Activities list is empty', _build_list_keyboard(available_actions)

    # Prefetching other necessary data, to prevent multiple queries for every activity
    Participant.clear_inactive()
    activities = pw.prefetch(activities, Participant, User)
    if user.has_right_to('p_summon'):
        available_actions.add('p_summon')

    response = 'Available activities:'
    for activity in activities:
        response += '\n\n*{0}*'.format(activity.name)

        is_subscribed = activity.subscription.id is not None
        available_actions.add('s_new' if is_subscribed else 's_delete')
        if activity.has_right_to_remove(user):
            available_actions.add('a_delete')
        if is_subscribed:
            response += '\n subscription active'

        if activity.participant_set_prefetch:
            online_users = [participant.user.telegram_login for participant in activity.participant_set_prefetch]
            response += '\n online: ' + ' '.join(online_users)
    return response, _build_list_keyboard(available_actions)


@personal_command('a_new')
def on_new(bot: tg.Bot, update: tg.Update, user: User):
    if user.pending_action not in {pending_user_actions['none'], pending_user_actions['a_new']}:
        u.on_cancel(bot, update, user)
    user.pending_action = pending_user_actions['a_new']
    user.save()
    return 'Send new activity name:', build_default_keyboard(user)


@personal_command('a_new')
def on_new_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error_message = Activity.try_to_create(update.message.text, user)
    if not activity:
        return 'Choose another name: ' + error_message

    user.pending_action = pending_user_actions['none']
    user.save()
    User.send_message_to_superuser(bot, text='{0} created activity *{1}*'.format(user.telegram_login, activity.name))
    return 'Activity *{0}* created'.format(activity.name), build_default_keyboard(user)


@personal_command('a_delete')
def on_delete(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select().order_by(Activity.name)
    if not user.is_superuser():
        activities = activities.where(Activity.owner == user)
    if not activities.exists():
        return 'Activities list is empty'

    return ('Select activity to remove:',
            build_inline_keyboard([[(x.name, 'a_delete ' + x.name)] for x in activities]))


@callback_only
@personal_command('a_delete')
def on_delete_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Removing selected activity...')
    if not activity:
        return error

    if not activity.has_right_to_remove(user):
        return 'You have not enough rights to remove *{0}*.'.format(activity.name)

    activity.delete_instance()
    return 'Activity *{0}* successfully deleted.'.format(activity.name)
