import telegram as tg

from .common import *
from ..models import *


@personal_command('activity_add')
def on_activity_add(bot: tg.Bot, update: tg.Update, user: User):
    user.pending_action = pending_user_actions['activity_add']
    user.save()
    inline_keyboard = tg.InlineKeyboardMarkup([[tg.InlineKeyboardButton(text='Cancel', callback_data='cancel')]])
    user.send_message(bot, text='Send new activity name:', reply_markup=inline_keyboard)


@personal_command('activity_add')
def on_activity_add_with_name(bot: tg.Bot, update: tg.Update, user: User):
    activity, error_message = Activity.try_to_create(update.message.text, user)
    if not activity:
        user.send_message(bot, text='Invalid name: ' + error_message)
    else:
        user.pending_action = pending_user_actions['none']
        user.save()
        user.send_message(bot, text='Activity *{0}* successfully created!'.format(activity.name))


@personal_command('activity_list')
def on_activity_list(bot: tg.Bot, update: tg.Update, user: User):
    del update  # Not used

    activities = Activity.select()
    inline_keyboard = None
    if not activities.exists():
        if user.has_right('activity_add'):
            inline_keyboard = tg.InlineKeyboardMarkup(
                [[tg.InlineKeyboardButton(text='Create new activity', callback_data='activity_add')]])
        user.send_message(bot, text='Activities list is empty.', reply_markup=inline_keyboard)
    else:
        actions = {'subscribe': False, 'unsubscribe': False, 'add': user.has_right('activity_add'), 'rem': False}
        response = 'Available activities:'
        for activity in activities:
            is_subscribed = Subscription.select().where((Subscription.user == user) &
                                                        (Subscription.activity == activity)).exists()
            if is_subscribed:
                actions['unsubscribe'] = True
            else:
                actions['subscribe'] = True
            if user.has_right('activity_rem') and activity.has_right_to_remove(user):
                actions['rem'] = True
            response += '\n - *{0}*{1}'.format(activity.name, ' (subscription active)' if is_subscribed else '')
        inline_keyboard = []
        if actions['subscribe']:
            inline_keyboard.append([tg.InlineKeyboardButton('New subscription', callback_data='subscribe')])
        if actions['unsubscribe']:
            inline_keyboard.append([tg.InlineKeyboardButton('Unsubscribe', callback_data='unsubscribe')])
        if actions['add']:
            inline_keyboard.append([tg.InlineKeyboardButton('Create activity', callback_data='activity_add')])
        if actions['rem']:
            inline_keyboard.append([tg.InlineKeyboardButton('Delete existing', callback_data='activity_rem')])
        user.send_message(bot, text=response, reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('activity_rem')
def on_activity_rem(bot: tg.Bot, update: tg.Update, user: User):
    del update  # Not used

    if user.telegram_login == superuser_login:
        activities = Activity.select()
    else:
        activities = Activity.select().where(Activity.owner == user)

    if not activities.exists():
        user.send_message(bot, text='No activities to remove.')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='activity_rem ' + x.name)] for x in activities]
    user.send_message(bot, text='Select activity to remove:', reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('activity_rem')
def on_activity_rem_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:  # Available only as callback
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    if not activity.has_right_to_remove(user):
        response = 'You have not enough rights to remove *{0}*.'.format(activity_name)
    else:
        activity.delete_instance()
        response = 'Activity *{0}* successfully deleted.'.format(activity_name)
    user.send_message(bot, text=response)
