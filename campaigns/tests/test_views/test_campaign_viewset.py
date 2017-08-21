from datetime import datetime

import recurrence
import json
from django.contrib.auth import get_user_model
from django.utils import timezone
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

        pattern = recurrence.Recurrence(
            dtstart=datetime(2014, 1, 2, 0, 0, 0),
            dtend=datetime(2014, 1, 3, 0, 0, 0),
            rrules=[r_rule, ]
        )

        obj = {
            "name": "My super awesome campaign",
            "description": "Super-cool campaign",
            "start": timezone.now(),
            "recurrence": pattern
        }

        print(json.dumps(obj))

        self.client.force_login(user=self.user1)
        r = self.client.post('/api/campaigns/', data=obj)
        print(r.content)



