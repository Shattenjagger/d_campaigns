import recurrence
from django.contrib.auth import get_user_model
from django.utils import timezone
from recurrence import serialize
from rest_framework.test import APITestCase

from campaigns.models import CustomAction


class CustomActionViewSetTests(APITestCase):
    def setUp(self):
        m = get_user_model()
        self.user1 = m.objects.create_user('test1', 'test1@test.com', 'super_password')
        self.user2 = m.objects.create_user('test2', 'test2@test.com', 'super_password')
        self.user1_actions = [
            CustomAction.objects.create(
                owner=self.user1,
                name="Custom action %s" % i,
                description="Custom action %s description" % i
            ) for i in range(0, 10)
        ]

        self.user2_actions = [
            CustomAction.objects.create(
                owner=self.user2,
                name="Custom action %s" % i,
                description="Custom action %s description" % i
            ) for i in range(0, 25)
        ]

    def test_should_have_api_accessible_for_auth_only(self):
        r = self.client.get('/api/custom_actions/')
        assert r.status_code == 403

        self.client.force_login(user=self.user1)
        r = self.client.get('/api/custom_actions/')
        assert r.status_code == 200

    def test_should_list_only_own_campaigns(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/custom_actions/')
        assert len(r.json()) == 10

        self.client.force_login(user=self.user2)
        r = self.client.get('/api/custom_actions/')
        assert len(r.json()) == 25

    def test_should_create_action(self):
        r_rule = recurrence.Rule(
            recurrence.DAILY
        )

        obj = {
            "name": "My super awesome action",
            "description": "Super-cool action",
            "start": timezone.now(),
            "rule": serialize(r_rule)
        }

        self.client.force_login(user=self.user1)
        r = self.client.post('/api/custom_actions/', data=obj)

        t = r.json()
        assert t['name'] == obj['name']

        o = CustomAction.objects.get(pk=t['id'])
        assert o.owner == self.user1

    def test_should_get_by_id(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/custom_actions/%s/' % self.user1_actions[0].id)
        assert r.status_code == 200

        r = self.client.get('/api/custom_actions/%s/' % self.user2_actions[0].id)
        assert r.status_code == 404

    def test_should_edit_action(self):
        new_name = 'Action edited'
        o = {
            "name": new_name
        }
        self.client.force_login(user=self.user1)
        r = self.client.patch('/api/custom_actions/%s/' % self.user1_actions[0].id, data=o)
        assert r.status_code == 200
        assert r.json()['name'] == new_name

        r = self.client.patch('/api/custom_actions/%s/' % self.user2_actions[0].id, data=o)
        assert r.status_code == 404

    def test_should_delete_action(self):
        self.client.force_login(user=self.user1)
        r = self.client.delete('/api/custom_actions/%s/' % self.user1_actions[0].id)
        assert r.status_code == 204

        r = self.client.delete('/api/custom_actions/%s/' % self.user2_actions[0].id)
        assert r.status_code == 404
