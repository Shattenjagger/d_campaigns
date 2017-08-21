from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class CampaignViewSetTests(APITestCase):
    def setUp(self):
        m = get_user_model()
        self.user1 = m.objects.create_user('test1', 'test1@test.com', 'super_password')

    def test_api_accessible(self):
        r = self.client.get('/api/campaigns/')
        assert r.status_code == 403

        self.client.force_login(user=self.user1)
        r = self.client.get('/api/campaigns/')
        assert r.status_code == 200
