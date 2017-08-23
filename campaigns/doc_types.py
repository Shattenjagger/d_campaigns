from django.conf import settings
from elasticsearch_dsl import DocType, Text, Integer, Nested, Date, Long


class SubscriptionObj(DocType):
    id = Long()
    user_id = Long()
    page_id = Long()
    subscription_uuid = Text()
    created = Date()
    modified = Date()
    start = Date()
    end = Date()
    status = Text()
    # payload = Nested()


class CampaignSubscriptionObj(SubscriptionObj):
    class Meta:
        index = settings.ES_CAMPAIGN_SUBSCRIBERS_IDX


class CustomActionSubscriptionObj(SubscriptionObj):
    class Meta:
        index = settings.ES_CUSTOM_ACTION_SUBSCRIBERS_IDX
