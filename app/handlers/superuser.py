from app.definitions import commands_by_level, superuser_login
from app.handlers.utils import *
from app.models.activity import Activity
from app.models.participant import Participant
from app.models.subscription import Subscription


@personal_command('su_full_information')
def on_full_information(bot: Bot, update: Update, user: User):
    # Users
    users = User.select()
    response = "User list:"
    for raw_user in users:
        response += "\n{0} : rights {1}, pending {2}, active: {3}, disabled: {4}".format(
            raw_user.telegram_login, raw_user.rights_level, raw_user.pending_action, raw_user.is_active,
            raw_user.is_disabled_chat)
    user.send_message(bot, text=response, reply_markup=InlineKeyboard([[('Promote', 'su_promote'),
                                                                        ('Demote', 'su_demote')]]))

    # Activities
    activities = Activity.select(Activity, User).join(User)
    response = "Activities list:"
    for activity in activities:
        response += "\n{0} - owner {1}".format(activity.name, activity.owner.telegram_login)
    user.send_message(bot, text=response)

    # Subscriptions
    subscriptions = Subscription.select(Activity, Subscription, User).join(Activity).join(User)
    response = "Subscriptions:"
    for subscription in subscriptions:
        response += "\n{0} to {1}".format(subscription.user.telegram_login, subscription.activity.name)
    user.send_message(bot, text=response)

    # Participants
    Participant.clear_inactive()
    participants = Participant.select(Activity, Participant, User).join(Activity).join(User)
    response = "Participants:"
    for participant in participants:
        response += "\n{0} in {1} ({2} from {3})".format(participant.user.telegram_login, participant.activity.name,
                                                         participant.is_accepted, participant.report_time)
    user.send_message(bot, text=response)


@callback_only
@personal_command('su_promote')
def on_promote(bot: Bot, update: Update, user: User):
    return _on_promote_impl(bot, update, user)


def _on_promote_impl(bot: Bot, update: Update, user: User):
    users = User.select().where((User.rights_level < len(commands_by_level) - 1) &
                                (User.telegram_login != superuser_login))
    if not users.exists():
        return 'No users to promote'

    return ('Select user to promote:',
            ClosableInlineKeyboard([[(x.telegram_login, 'su_promote ' + str(x.telegram_user_id))] for x in users],
                                   'Close selection'))


@callback_only
@personal_command('su_promote')
def on_promote_with_data(bot: Bot, update: Update, user: User):
    promote_messages = [
        '',
        'You have been promoted!\n\nRights to manage activities and summon friends added.',
    ]

    telegram_id = CallbackUtil.get_data(update.callback_query.data)
    selected_user = User.get(User.telegram_user_id == telegram_id)
    if selected_user.rights_level == len(commands_by_level) - 1:
        return selected_user.telegram_login + ' has maximum rights already'
    selected_user.rights_level += 1
    selected_user.save()
    selected_user.send_message(bot,
                               text=promote_messages[selected_user.rights_level],
                               reply_markup=UserKeyboard(selected_user))
    CallbackUtil.update_selection(bot, update, _on_promote_impl(bot, update, user))
    return '{0} promoted to rights level {1}'.format(selected_user.telegram_login, selected_user.rights_level)


@callback_only
@personal_command('su_demote')
def on_demote(bot: Bot, update: Update, user: User):
    return _on_demote_impl(bot, update, user)


def _on_demote_impl(bot: Bot, update: Update, user: User):
    users = User.select().where((User.rights_level > 0) & (User.telegram_login != superuser_login))
    if not users.exists():
        return 'No users to demote'

    return ('Select user to demote:',
            ClosableInlineKeyboard([[(x.telegram_login, 'su_demote ' + str(x.telegram_user_id))] for x in users],
                                   'Close selection'))


@callback_only
@personal_command('su_demote')
def on_demote_with_data(bot: Bot, update: Update, user: User):
    demote_messages = [
        'You have been demoted!\n\nRights to manage activities and summon friends removed.',
        '',
    ]

    telegram_id = CallbackUtil.get_data(update.callback_query.data)
    selected_user = User.get(User.telegram_user_id == telegram_id)
    if selected_user.rights_level == 0:
        return selected_user.telegram_login + ' has default rights already'
    selected_user.rights_level -= 1
    selected_user.save()
    selected_user.send_message(bot,
                               text=demote_messages[selected_user.rights_level],
                               reply_markup=UserKeyboard(selected_user))
    CallbackUtil.update_selection(bot, update, _on_demote_impl(bot, update, user))
    return '{0} demoted to rights level {1}'.format(selected_user.telegram_login, selected_user.rights_level)
