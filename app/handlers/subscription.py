import telegram as tg

from app.handlers.utils import *
from app.models import *


@personal_command('s_new')
def on_new(bot: tg.Bot, update: tg.Update, user: User):
    return _on_new_impl(bot, update, user)


def _on_new_impl(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription, join_type=pw.JOIN_LEFT_OUTER,
                        on=((Subscription.activity == Activity.id) & (Subscription.user == user)))
                  .where(Subscription.id.is_null(True))
                  .order_by(Activity.name))
    if not activities:
        return 'No activities available for subscription.'

    return ('Select activity to subscribe:',
            ClosableInlineKeyboard([[(x.name, 's_new ' + x.name)] for x in activities], 'Close selection'))


@callback_only
@personal_command('s_new')
def on_new_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        CallbackUtil.edit(update, error)
        return

    _, is_created = Subscription.get_or_create(activity=activity, user=user)
    if is_created:
        participants = Participant.select_participants_for_activity(activity, user)
        if participants:
            user.send_message(bot,
                              text='There is active {0} session!\n'
                                   'Already joined: {1}\n'
                                   'Want to join too?'.format(
                                        activity.name_md(), ', '.join([p.telegram_login for p in participants])),
                              reply_markup=ResponseInlineKeyboard(activity.name))

    CallbackUtil.update_selection(bot, update, _on_new_impl(bot, update, user))
    return 'Subscription to {0} enabled.'.format(activity.name_md())


@personal_command('s_delete')
def on_delete(bot: tg.Bot, update: tg.Update, user: User):
    return _on_delete_impl(bot, update, user)


def _on_delete_impl(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription)
                  .where(Subscription.user == user)
                  .order_by(Activity.name))
    if not activities.exists():
        return 'Subscriptions list is empty.'

    return ('Select activity to unsubscribe:',
            ClosableInlineKeyboard([[(x.name, 's_delete ' + x.name)] for x in activities], 'Close selection'))


@callback_only
@personal_command('s_delete')
def on_delete_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(CallbackUtil.get_data(update.callback_query.data))
    if not activity:
        return error

    Subscription.delete().where((Subscription.activity == activity) & (Subscription.user == user)).execute()
    CallbackUtil.update_selection(bot, update, _on_delete_impl(bot, update, user))
    return 'Subscription to {0} disabled.'.format(activity.name_md())
