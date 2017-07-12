import telegram as tg
import peewee as pw

from .common import *
from ..models import *


@personal_command('activity_add')
def on_activity_add(bot: tg.Bot, update: tg.Update, user: User):
    user.pending_action = pending_user_actions['activity_add']
    user.save()
    return 'Send new activity name:', build_inline_keyboard([[('Cancel', 'cancel')]])


@personal_command('activity_add')
def on_activity_add_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error_message = Activity.try_to_create(update.message.text, user)
    if not activity:
        return 'Invalid name: ' + error_message

    user.pending_action = pending_user_actions['none']
    user.save()
    return 'Activity *{0}* created'.format(activity.name)


@personal_command('activity_list')
def on_activity_list(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription, pw.JOIN_LEFT_OUTER)
                  .where((Subscription.id.is_null(True)) | (Subscription.user == user))
                  .order_by(Activity.name))
    if not activities.exists():
        return ('Activities list is empty',
                build_inline_keyboard([[('Create new', 'activity_add')]]) if user.has_right('activity_add') else None)

    actions = {'subscribe': False, 'unsubscribe': False, 'add': user.has_right('activity_add'), 'rem': False}
    response = 'Available activities:'
    for activity in activities:
        is_subscribed = activity.subscription.id is not None
        actions['unsubscribe'] |= is_subscribed
        actions['subscribe'] |= not is_subscribed
        actions['rem'] |= activity.has_right_to_remove(user)
        response += '\n - *{0}*{1}'.format(activity.name, ' (subscription active)' if is_subscribed else '')
    buttons = []
    if actions['subscribe']:
        buttons.append([('New subscription', 'subscribe')])
    if actions['unsubscribe']:
        buttons.append([('Unsubscribe', 'unsubscribe')])
    if actions['add']:
        buttons.append([('Create activity', 'activity_add')])
    if actions['rem']:
        buttons.append([('Delete existing', 'activity_rem')])
    return response, build_inline_keyboard(buttons)


@personal_command('activity_rem')
def on_activity_rem(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select().order_by(Activity.name)
    if user.telegram_login != superuser_login:
        activities = activities.where(Activity.owner == user)
    if not activities.exists():
        return 'Activities list is empty'

    return ('Select activity to remove:',
            build_inline_keyboard([[(x.name, 'activity_rem ' + x.name)] for x in activities]))


@callback_only
@personal_command('activity_rem')
def on_activity_rem_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        return 'Activity *{0}* not found.'.format(activity_name)

    if not activity.has_right_to_remove(user):
        return 'You have not enough rights to remove *{0}*.'.format(activity_name)

    activity.delete_instance()
    return 'Activity *{0}* successfully deleted.'.format(activity_name)
