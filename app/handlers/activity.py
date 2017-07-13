import telegram as tg

from .utils import *
from ..models import *


@personal_command('a_list')
def on_list(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription, pw.JOIN_LEFT_OUTER)
                  .where((Subscription.id.is_null(True)) | (Subscription.user == user))
                  .order_by(Activity.name))
    if not activities.exists():
        return ('Activities list is empty',
                build_inline_keyboard([[('Create new', 'a_new')]]) if user.has_right('a_new') else None)

    actions = {'s_new': False, 's_delete': False, 'a_delete': False}
    response = 'Available activities:'
    Participant.clear_inactive()
    for activity in activities:
        is_subscribed = activity.subscription.id is not None
        actions['s_delete'] |= is_subscribed
        actions['s_new'] |= not is_subscribed
        actions['a_delete'] |= activity.has_right_to_remove(user)
        response += '\n\n - *{0}*'.format(activity.name)
        if is_subscribed:
            response += '\n   subscription active'
        current_participants = (Participant.select(Participant, User)
                                           .where(Participant.activity == activity).join(User))
        if current_participants.exists():
            response += '\n   online: ' + ' '.join([x.user.telegram_login for x in current_participants])
    buttons = []
    if user.has_right('p_summon'):
        buttons.append([('Summon people', 'p_summon')])
    if actions['s_new']:
        buttons.append([('New subscription', 's_new')])
    if actions['s_delete']:
        buttons.append([('Unsubscribe', 's_delete')])
    if user.has_right('a_new'):
        buttons.append([('Create activity', 'a_new')])
    if actions['a_delete']:
        buttons.append([('Delete existing', 'a_delete')])
    return response, build_inline_keyboard(buttons)


@personal_command('a_new')
def on_new(bot: tg.Bot, update: tg.Update, user: User):
    user.pending_action = pending_user_actions['a_new']
    user.save()
    return 'Send new activity name:', build_default_keyboard(user)


@personal_command('a_new')
def on_new_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error_message = Activity.try_to_create(update.message.text, user)
    if not activity:
        return 'Invalid name: ' + error_message

    user.pending_action = pending_user_actions['none']
    user.save()
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
    activity, error = Activity.get_by_name(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Removing selected activity...')

    if not activity:
        return error

    if not activity.has_right_to_remove(user):
        return 'You have not enough rights to remove *{0}*.'.format(activity.name)

    activity.delete_instance()
    return 'Activity *{0}* successfully deleted.'.format(activity.name)
