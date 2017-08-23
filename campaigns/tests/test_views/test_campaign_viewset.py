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

    def test_should_create_campaign(self):
        r_rule = recurrence.Rule(
            recurrence.DAILY
        )

        pattern = recurrence.Recurrence(rrules=[r_rule, ])

        obj = {
            "name": "My super awesome campaign",
            "description": "Super-cool campaign",
            "start": timezone.now(),
            "recurrence": serialize(pattern)
        }

        self.client.force_login(user=self.user1)
        r = self.client.post('/api/campaigns/', data=obj)

        t = r.json()
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



