import telegram as tg

from ..models import *
from .common import personal_command


@personal_command('subscribe')
def on_subscribe(bot: tg.Bot, update: tg.Update, user: User):
    subscribed_activities = [x.name for x in Activity.select().join(Subscriber).where(Subscriber.user == user)]
    if len(subscribed_activities) > 0:
        activities = Activity.select().where(Activity.name.not_in(subscribed_activities))
    else:
        activities = Activity.select()
    if not activities.exists():
        user.send_message(bot, text='There are no activities you can subscribe to.')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='subscribe ' + x.name)] for x in activities]
    user.send_message(bot, text='Select activity to subscribe:', reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('subscribe')
def on_subscribe_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    if Subscriber.select().where((Subscriber.activity == activity) & (Subscriber.user == user)).count() > 0:
        user.send_message(bot, text='You have been subscribed already.')
        return
    Subscriber.create(activity=activity, user=user)
    user.send_message(bot, text='You have successfully subscribed to *{0}*.'.format(activity.name))


@personal_command('unsubscribe')
def on_unsubscribe(bot: tg.Bot, update: tg.Update, user: User):
    activities = Activity.select().join(Subscriber).where(Subscriber.user == user)
    if len(activities) == 0:
        user.send_message(bot, text='There are no activities you can unsubscribe from.')
        return
    inline_keyboard = [[tg.InlineKeyboardButton(x.name, callback_data='unsubscribe ' + x.name)] for x in activities]
    user.send_message(bot, text='Select activity to unsubscribe:', reply_markup=tg.InlineKeyboardMarkup(inline_keyboard))


@personal_command('unsubscribe')
def on_unsubscribe_with_name(bot: tg.Bot, update: tg.Update, user: User):
    if not update.callback_query:
        return
    activity_name = update.callback_query.data.split(' ', 1)[1]
    try:
        activity = Activity.get(Activity.name == activity_name)
    except Activity.DoesNotExist:
        user.send_message(bot, text='Activity *{0}* not found.'.format(activity_name))
        return
    try:
        subscriber = Subscriber.get((Subscriber.user == user) & (Subscriber.activity == activity))
    except Subscriber.DoesNotExist:
        user.send_message(bot, text='You are not subscribed to *{0}*.'.format(activity_name))
        return
    subscriber.delete_instance()
    user.send_message(bot, text='You have successfully unsubscribed from *{0}*.'.format(activity.name))
