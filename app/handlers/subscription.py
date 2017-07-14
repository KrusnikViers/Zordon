import telegram as tg

from ..models import *
from .utils import *


@personal_command('s_new')
def on_new(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription, pw.JOIN_LEFT_OUTER)
                  .where(Subscription.id.is_null(True))
                  .order_by(Activity.name))
    if not activities:
        return 'No activities available for subscription'

    return ('Select activity to subscribe:',
            build_inline_keyboard([[(x.name, 's_new ' + x.name)] for x in activities]))


@callback_only
@personal_command('s_new')
def on_new_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Subscribing...')
    if not activity:
        return error

    _, is_created = Subscription.get_or_create(activity=activity, user=user)
    if is_created:
        Participant.clear_inactive()
        if Participant.select(Participant).where(Participant.activity == activity).exists():
            user.send_message(bot,
                              text='Summon is active for *{1}*',
                              reply_markup=build_summon_response_keyboard(activity.name))
    return 'Subscription to *{0}* enabled'.format(activity.name)


@personal_command('s_delete')
def on_delete(bot: tg.Bot, update: tg.Update, user: User):
    activities = (Activity
                  .select(Activity, Subscription)
                  .join(Subscription)
                  .where(Subscription.user == user)
                  .order_by(Activity.name))
    if not activities.exists():
        return 'No activities to unsubscribe from.'

    return ('Select activity to unsubscribe:',
            build_inline_keyboard([[(x.name, 's_delete ' + x.name)] for x in activities]))


@callback_only
@personal_command('s_delete')
def on_delete_with_data(bot: tg.Bot, update: tg.Update, user: User):
    activity, error = Activity.try_to_get(get_info_from_callback_data(update.callback_query.data))
    edit_callback_message(update, 'Removing subscription...')
    if not activity:
        return error

    Subscription.delete().where((Subscription.activity == activity) & (Subscription.user == user)).execute()
    return 'Subscription to *{0}* disabled'.format(activity.name)
