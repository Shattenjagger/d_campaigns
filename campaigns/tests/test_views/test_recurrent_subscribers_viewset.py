from time import sleep

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
from rest_framework.test import APITestCase

from campaigns.doc_types import CampaignSubscriptionObj, CustomActionSubscriptionObj
from campaigns.models import CustomAction, Campaign


class RecurrentSubscribersViewSetTests(APITestCase):
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

        self.other_users = [
            m.objects.create_user('other_test_%s' % k, 'other_test_%s@test.com' % k, 'super_password') for k in
            range(0, 10)
            ]

        self.es = Elasticsearch(settings.ES_CLUSTER)

        c_a_idx_data = [
            {
                'user_id': u.id,
                'page_id': 0,
                'subscription_uuid': self.user1_actions[0].uuid,
                'start': None,
                'end': None,
                'created': timezone.now(),
                'modified': timezone.now(),
                'payload': {
                    'data': 'Super-awesome'
                },
                'status': 'active'
            } for u in self.other_users
            ]

        c_idx_data = [
            {
                'user_id': u.id,
                'page_id': 0,
                'subscription_uuid': self.user1_campaigns[0].uuid,
                'start': None,
                'end': None,
                'created': timezone.now(),
                'modified': timezone.now(),
                'payload': {
                    'data': 'Super-awesome'
                },
                'status': 'active'
            } for u in self.other_users
            ]

        self.campaign_idx = Index(settings.ES_CAMPAIGN_SUBSCRIBERS_IDX, using=self.es)
        self.custom_action_idx = Index(settings.ES_CUSTOM_ACTION_SUBSCRIBERS_IDX, using=self.es)
        self.campaign_idx.doc_type(CampaignSubscriptionObj)
        self.custom_action_idx.doc_type(CustomActionSubscriptionObj)

        for u in self.other_users:
            c = CampaignSubscriptionObj(
                user_id=u.id,
                page_id=0,
                subscription_uuid=self.user1_campaigns[0].uuid,
                start=None,
                end=None,
                created=timezone.now(),
                modified=timezone.now(),
                status='active'
            )
            c.save(using=self.es)

            c = CustomActionSubscriptionObj(
                user_id=u.id,
                page_id=0,
                subscription_uuid=self.user1_actions[0].uuid,
                start=None,
                end=None,
                created=timezone.now(),
                modified=timezone.now(),
                status='active'
            )
            c.save(using=self.es)
            sleep(1)

    def tearDown(self):
        self.campaign_idx.delete(ignore=404)
        self.custom_action_idx.delete(ignore=404)

    def test_should_list_subsribers(self):
        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/%s/subscribers/' % self.user1_campaigns[0].uuid)

        assert r.status_code == 200
        assert len(r.json()) == 10

        r = self.client.get('/api/custom_actions/%s/subscribers/' % self.user1_actions[0].uuid)
        assert r.status_code == 200
        assert len(r.json()) == 10

    def test_should_create_new(self):
        m = get_user_model()
        new_user = m.objects.create_user('new_test_user', 'new_test_user@test.com', 'super_password')
        obj = {
            'user_id': new_user.id,
            'page_id': 0,
            'subscription_uuid': self.user1_actions[0].uuid,
            'start': timezone.now(),
            'end': timezone.now(),
            'status': 'active'
        }

        self.client.force_login(user=self.user1)

        r = self.client.post('/api/custom_actions/%s/subscribers/' % self.user1_actions[0].uuid, data=obj)
        assert r.status_code == 201

    def test_should_destroy(self):
        self.client.force_login(user=self.user1)
        r = self.client.delete('/api/custom_actions/%s/subscribers/%s/' % (self.user1_actions[0].uuid, self.other_users[0].id))
        assert r.status_code == 204

    def test_should_update(self):
        obj = {
            'page_id': 0,
            'subscription_uuid': self.user1_actions[0].uuid,
            'start': timezone.now(),
            'end': timezone.now(),
            'status': 'active'
        }

        self.client.force_login(user=self.user1)
        r = self.client.put('/api/custom_actions/%s/subscribers/%s/' % (self.user1_actions[0].uuid, self.other_users[0].id), data=obj)
        assert r.status_code == 200
