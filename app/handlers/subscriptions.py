import telegram as tg

from ..models import *
from .common import personal_command


@personal_command('subscribe')
def on_subscribe(bot: tg.Bot, update: tg.Update, user: User):
    user_activities = Activity.select().join(Subscription).where(Subscription.user == user)
    if user_activities.exists():
        activities = Activity.select().where(Activity.name.not_in([x.name for x in user_activities]))
    else:
        activities = Activity.select()
    if not activities.exists():
        user.send_message(bot, text='No activities available for subscription.')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='subscribe ' + x.name)] for x in activities]
    user.send_message(bot, text='Select activity to subscribe:', reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('subscribe')
def on_subscribe_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:  # Available only as callback
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    if Subscription.select().where((Subscription.activity == activity) & (Subscription.user == user)).exists():
        user.send_message(bot, text='Already subscribed to *{0}*.'.format(activity_name))
        return
    Subscription.create(activity=activity, user=user)
    user.send_message(bot, text='Successfully subscribed to *{0}*.'.format(activity_name))


@personal_command('unsubscribe')
def on_unsubscribe(bot: tg.Bot, update: tg.Update, user: User):
    del update  # Not used

    activities = Activity.select().join(Subscription).where(Subscription.user == user)
    if not activities.exists():
        user.send_message(bot, text='No activities available.')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='unsubscribe ' + x.name)] for x in activities]
    user.send_message(bot, text='Select activity to unsubscribe:', reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('unsubscribe')
def on_unsubscribe_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:  # Available only as callback.
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    try:
        subscriber = Subscription.get((Subscription.user == user) & (Subscription.activity == activity))
    except Subscription.DoesNotExist:
        user.send_message(bot, text='Not subscribed to *{0}*.'.format(activity_name))
        return
    subscriber.delete_instance()
    user.send_message(bot, text='Successfully unsubscribed from *{0}*.'.format(activity.name))
