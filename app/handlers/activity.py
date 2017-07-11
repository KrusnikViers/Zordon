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
        print(error_message)
        user.send_message(bot, text='Try again: ' + error_message)
    else:
        user.pending_action = pending_user_actions['none']
        user.save()
        user.send_message(bot, text='Activity *{0}* successfully created!'.format(activity.name))


@personal_command('activity_list')
def on_activity_list(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select()
    inline_keyboard = None
    if len(activities) == 0:
        if user.has_right('activity_add'):
            inline_keyboard = tg.InlineKeyboardMarkup(
                [[tg.InlineKeyboardButton(text='Create new activity', callback_data='activity_add')]])
        user.send_message(bot, text='There are no activities at the moment.', reply_markup=inline_keyboard)
    else:
        possible_actions = {'subscribe': False,
                            'unsubscribe': False,
                            'add': user.has_right('activity_add'),
                            'rem': False}
        response = 'Available activities:'
        for i in range(0, len(activities)):
            activity = activities[i]
            is_subscribed = Subscriber.select().where(Subscriber.user == user).count() == 1
            if is_subscribed:
                possible_actions['unsubscribe'] = True
            else:
                possible_actions['subscribe'] = True
            if user.has_right('activity_rem') and activity.has_right_to_remove(user):
                possible_actions['rem'] = True
            response += '\n - *{0}*{1}'.format(activity.name, ' (subscription active)' if is_subscribed else '')
        inline_keyboard = []
        if possible_actions['subscribe']:
            inline_keyboard.append([tg.InlineKeyboardButton('New subscription', callback_data='subscribe')])
        if possible_actions['unsubscribe']:
            inline_keyboard.append([tg.InlineKeyboardButton('Unsubscribe', callback_data='unsubscribe')])
        if possible_actions['add']:
            inline_keyboard.append([tg.InlineKeyboardButton('Create activity', callback_data='activity_add')])
        if possible_actions['rem']:
            inline_keyboard.append([tg.InlineKeyboardButton('Delete existing', callback_data='activity_rem')])
        user.send_message(bot, text=response, reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('activity_rem')
def on_activity_rem(bot: tg.Bot, update: tg.Update, user: User):
    if user.telegram_login == superuser_login:
        activities = Activity.select()
    else:
        activities = Activity.select().where(Activity.owner == user)

    if len(activities) == 0:
        user.send_message(bot, text='There are no activities you can remove')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='activity_rem ' + x.name)]
                       for x in activities]
    user.send_message(bot,
                      text='Please, select activity to remove:',
                      reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('activity_rem')
def on_activity_rem_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    if not activity.has_right_to_remove(user):
        user.send_message(bot, text='You have not enough rights to remove *{0}*.'.format(activity_name))
        return
    activity.delete_instance()
    user.send_message(bot, text='Activity *{0}* successfully deleted.'.format(activity_name))
