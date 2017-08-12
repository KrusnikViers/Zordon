from unittest.mock import create_autospec
from telegram import Bot
import datetime

from app.definitions import cooldown_time_minutes
from app.models.activity import Activity
from app.models.participant import Participant
from app.models.subscription import Subscription
from app.models.user import User
from tests.base_test import BaseTestCase


class TestParticipantModel(BaseTestCase):
    def setUp(self):
        super(TestParticipantModel, self).setUp()
        self.users = [User.create(telegram_user_id=i) for i in range(0, 15) if i != 5]
        self.activities = [Activity.create(name=str(i), owner=self.users[i]) for i in range(0, 4)]

    def test_clear_inactive(self):
        cooldown_delta = datetime.timedelta(minutes=cooldown_time_minutes + 5)
        is_accepted = True
        for user in self.users:
            is_accepted = not is_accepted
            report_time = datetime.datetime.now() - cooldown_delta + datetime.timedelta(minutes=user.telegram_user_id)
            Participant.create(user=user, activity=self.activities[0], is_accepted=is_accepted, report_time=report_time)
        self.assertEqual(14, Participant.select().count())
        Participant.clear_inactive()
        self.assertEqual(9, Participant.select().count())

    def test_clear_inactive_and_declined(self):
        self.assertLess(len(self.activities), len(self.users))
        n = len(self.activities)
        for i in range(0, n):
            for j in range(0, n):
                # Two last activities won't have any accepted participants
                Participant.create(activity=self.activities[i], user=self.users[j], is_accepted=(i + 1 < j))
        Participant.clear_inactive()
        for i in range(0, n):
            if i + 2 < n:
                self.assertEqual(n, Participant.select().where(Participant.activity == self.activities[i]).count())
            else:
                self.assertFalse(Participant.select().where(Participant.activity == self.activities[i]).exists())

    def test_select_participants(self):
        for user in self.users:
            case = user.telegram_user_id % (len(self.activities) + 1)
            if case < len(self.activities):
                Participant.create(activity=self.activities[case], user=user)
        # Only 10th user - zero user does not count itself
        self.assertEqual(1, Participant.select_participants_for_activity(self.activities[0], self.users[0]).count())
        # 1st, 6th and 11th users
        self.assertEqual(3, Participant.select_participants_for_activity(self.activities[1], self.users[0]).count())

    def test_select_subscribers(self):
        for user in self.users:
            activity = self.activities[user.telegram_user_id % len(self.activities)]
            taking_part = user.telegram_user_id % 3 == 0
            Subscription.create(activity=activity, user=user)
            if taking_part:
                Participant.create(activity=activity, user=user)

        # 4th and 8th users (zero and 12 users are already participants)
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[0]).count())
        # 1 and 13 (without 9)
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[1]).count())
        # 2, 10 and 14 (without 6)
        self.assertEqual(3, Participant.select_subscribers_for_activity(self.activities[2]).count())
        # 7 and 11 (without 3) - and check it for the last selection
        self.assertEqual(2, Participant.select_subscribers_for_activity(self.activities[3]).count())
        for participant in Participant.select_subscribers_for_activity(self.activities[3]):
            self.assertTrue(participant.telegram_user_id in {7, 11})

    def test_response_to_summon(self):
        prev = Participant.create(activity=self.activities[0], user=self.users[1])
        cur = Participant.create(activity=self.activities[0], user=self.users[0])
        bot_mock = create_autospec(Bot)

        Participant.response_to_summon(bot_mock, self.users[0], self.activities[0], 'p_decline')
        bot_mock.send_message.assert_called_once_with(chat_id=1, text=' declined summon for 0')
        cur = Participant.get(activity=self.activities[0], user=self.users[0])
        self.assertFalse(cur.is_accepted)
