from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from campaigns.models import Campaign


class CampaignTests(TestCase):

    def test_should_generate_proper_recurrences(self):
        m = get_user_model()
        u = m.objects.create_user('test1', 'test1@test.com', 'super_password')
        c = Campaign.objects.create(
            owner=u,
            name="Campaign",
            description="Campaign description",
            start=timezone.now()
        )

        print(c.recurrence)
