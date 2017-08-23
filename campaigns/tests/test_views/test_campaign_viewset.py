import celery
import recurrence
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone
from recurrence import serialize
from redbeat import RedBeatSchedulerEntry
from rest_framework.test import APITestCase

from campaigns.models import Campaign


class CampaignViewSetTests(APITestCase):
    def setUp(self):
        m = get_user_model()
        self.user1 = m.objects.create_user('test1', 'test1@test.com', 'super_password')
        self.user2 = m.objects.create_user('test2', 'test2@test.com', 'super_password')
        self.user1_campaigns = [
            Campaign.objects.create(
                owner=self.user1,
                name="Campaign %s" % i,
                description="Campaign %s description" % i,
                start=timezone.now()
            ) for i in range(0, 10)
            ]

        self.user2_campaigns = [
            Campaign.objects.create(
                owner=self.user2,
                name="Campaign %s" % i,
                description="Campaign %s description" % i,
                start=timezone.now()
            ) for i in range(0, 25)
            ]

    def test_should_have_api_accessible_for_auth_only(self):
        r = self.client.get('/api/campaigns/')
        assert r.status_code == 403

        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/')
        assert r.status_code == 200

    def test_should_list_only_own_campaigns(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/')
        assert len(r.json()) == 10

        self.client.force_login(user=self.user2)
        r = self.client.get('/api/campaigns/')
        assert len(r.json()) == 25

    # noinspection PyMethodMayBeStatic
    def test_should_generate_proper_recurrence_rules(self):
        """
            Basically it's not a regular test, but short tip-list about how RRules being serialized
        """

        # Every day
        r = recurrence.Rule(
            recurrence.DAILY
        )
        assert serialize(r) == 'RRULE:FREQ=DAILY'

        # Every second day
        r = recurrence.Rule(
            recurrence.DAILY,
            interval=2
        )
        assert serialize(r) == 'RRULE:FREQ=DAILY;INTERVAL=2'

        # Every week
        r = recurrence.Rule(
            recurrence.WEEKLY
        )
        assert serialize(r) == 'RRULE:FREQ=WEEKLY'

        # Every second week
        r = recurrence.Rule(
            recurrence.WEEKLY,
            interval=2
        )
        assert serialize(r) == 'RRULE:FREQ=WEEKLY;INTERVAL=2'

        # Every second week on Wednesdays
        r = recurrence.Rule(
            recurrence.WEEKLY,
            interval=2,
            byday=2
        )
        assert serialize(r) == 'RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=WE'

        # Every month on 11th day
        r = recurrence.Rule(
            recurrence.MONTHLY,
            interval=1,
            bymonthday=11
        )
        assert serialize(r) == 'RRULE:FREQ=MONTHLY;BYMONTHDAY=11'

        # Every month on second Sunday
        r = recurrence.Rule(
            recurrence.MONTHLY,
            interval=1,
            byday=6,
            bysetpos=2
        )
        assert serialize(r) == 'RRULE:FREQ=MONTHLY;BYDAY=SU;BYSETPOS=2'

        # Every year on 11th of July
        r = recurrence.Rule(
            recurrence.YEARLY,
            interval=1,
            bymonth=recurrence.JULY,
            bymonthday=11
        )
        assert serialize(r) == 'RRULE:FREQ=YEARLY;BYMONTH=7;BYMONTHDAY=11'

        # Every second Sunday of June
        r = recurrence.Rule(
            recurrence.YEARLY,
            interval=1,
            bymonth=recurrence.JUNE,
            byday=6,
            bysetpos=2
        )
        assert serialize(r) == 'RRULE:FREQ=YEARLY;BYDAY=SU;BYSETPOS=2;BYMONTH=6'

    def test_should_create_campaign(self):
        r_rule = recurrence.Rule(
            recurrence.DAILY
        )

        obj = {
            "name": "My super awesome campaign",
            "description": "Super-cool campaign",
            "start": timezone.now(),
            "rule": serialize(r_rule)
        }
        print(obj)

        self.client.force_login(user=self.user1)
        r = self.client.post('/api/campaigns/', data=obj)

        t = r.json()
        print(t)
        assert t['name'] == obj['name']

        o = Campaign.objects.get(pk=t['id'])
        assert o.owner == self.user1

    def test_should_get_by_id(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/%s/' % self.user1_campaigns[0].id)
        assert r.status_code == 200

        r = self.client.get('/api/campaigns/%s/' % self.user2_campaigns[0].id)
        assert r.status_code == 404

    def test_should_edit_campaign(self):
        new_name = 'Campaign edited'
        o = {
            "name": new_name
        }
        self.client.force_login(user=self.user1)
        r = self.client.patch('/api/campaigns/%s/' % self.user1_campaigns[0].id, data=o)
        assert r.status_code == 200
        assert r.json()['name'] == new_name

        r = self.client.patch('/api/campaigns/%s/' % self.user2_campaigns[0].id, data=o)
        assert r.status_code == 404

    def test_should_delete_campaign(self):
        self.client.force_login(user=self.user1)
        r = self.client.delete('/api/campaigns/%s/' % self.user1_campaigns[0].id)
        assert r.status_code == 204

        r = self.client.delete('/api/campaigns/%s/' % self.user1_campaigns[0].id)
        assert r.status_code == 404

    def test_should_activate(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/%s/activate/' % self.user1_campaigns[0].id)
        assert r.status_code == 200

        r = self.client.get('/api/campaigns/%s/activate/' % self.user2_campaigns[0].id)
        assert r.status_code == 404

    def test_should_deactivate(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/%s/deactivate/' % self.user1_campaigns[0].id)
        assert r.status_code == 200

        r = self.client.get('/api/campaigns/%s/deactivate/' % self.user2_campaigns[0].id)
        assert r.status_code == 404

        # @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
        # def test_redbeat(self):
        #     from d_campaigns import celery_app
        #     interval = celery.schedules.schedule(run_every=5)  # seconds
        #     entry = RedBeatSchedulerEntry('task-name-2', 'campaigns.tasks.add', interval, args=[5, 2], app=celery_app)
        #     entry.save()
        #
        # @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
        # def test_redbeat_delete(self):
        #     from d_campaigns import celery_app
        #     interval = celery.schedules.schedule(run_every=5)  # seconds
        #     entry = RedBeatSchedulerEntry('task-name-2', 'campaigns.tasks.add', interval, args=[5, 2], app=celery_app)
        #     entry.delete()
