from telegram import Bot
import datetime
from peewee import BooleanField, ForeignKeyField, TimestampField, JOIN_LEFT_OUTER

from app.definitions import cooldown_time_minutes
from app.models.activity import Activity
from app.models.base import BaseModel
from app.models.subscription import Subscription
from app.models.user import User


class Participant(BaseModel):
    """ User, agreed to take part in some activity """
    report_time = TimestampField(default=datetime.datetime.now)
    is_accepted = BooleanField(default=True)
    user = ForeignKeyField(User, on_delete='CASCADE')
    activity = ForeignKeyField(Activity, on_delete='CASCADE')

    @classmethod
    def clear_inactive(cls):
        time_lower_bound = datetime.datetime.now() - datetime.timedelta(minutes=cooldown_time_minutes)
        Participant.delete().where(Participant.report_time < time_lower_bound).execute()

        # Remove all sessions without active participants
        active_session_activities = (Activity.select().join(Participant).where(Participant.is_accepted == True)
                                     .group_by(Activity))
        Participant.delete().where(Participant.activity.not_in(active_session_activities)).execute()

    @classmethod
    def select_participants_for_activity(cls, activity: Activity, user: User):
        Participant.clear_inactive()
        return User.select().where(~User.is_disabled_chat).join(Participant).where((Participant.activity == activity) &
                                                                                   (Participant.user != user) &
                                                                                   (Participant.is_accepted == True))

    @classmethod
    def select_subscribers_for_activity(cls, activity: Activity):
        Participant.clear_inactive()
        return (User.select().where((User.is_active) & (~User.is_disabled_chat))
                .join(Subscription).where(Subscription.activity == activity).switch(User)
                .join(Participant, JOIN_LEFT_OUTER).where(Participant.id.is_null(True)))

    @classmethod
    def response_to_summon(cls, bot: Bot, user: User, activity: Activity, join_mode: str):
        cls.clear_inactive()
        is_accepted = join_mode != 'p_decline'
        messages = {'p_accept': '{0} join you in {1}',
                    'p_accept_later': '{0} will join you in {1} in a short while',
                    'p_decline': '{0} declined summon for {1}',
                    'p_summon': '{0} join you in {1} with new summon call'}
        participant, was_created = cls.get_or_create(activity=activity, user=user,
                                                     defaults={'is_accepted': is_accepted})
        if was_created or is_accepted is not participant.is_accepted:
            for active_user in cls.select_participants_for_activity(activity, user):
                active_user.send_message(bot, text=messages[join_mode].format(user.telegram_login, activity.name))
        if not was_created:
            participant.is_accepted = is_accepted
            participant.report_time = datetime.datetime.now()
            participant.save()
