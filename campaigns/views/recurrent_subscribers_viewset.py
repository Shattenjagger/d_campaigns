import json

from django.utils import timezone
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from campaigns.doc_types import CustomActionSubscriptionObj, CampaignSubscriptionObj


class RecurrentSubscribersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get_index_and_uuid(**kwargs):
        if 'campaign_pk' in kwargs:
            return CampaignSubscriptionObj, kwargs['campaign_pk']
        if 'custom_action_pk' in kwargs:
            return CustomActionSubscriptionObj, kwargs['custom_action_pk']
        return None, None

    def list(self, request, *args, **kwargs):
        idx_obj, uuid = self.get_index_and_uuid(**kwargs)
        es = Elasticsearch(settings.ES_CLUSTER)
        s = idx_obj.search(using=es).query('match', subscription_uuid=uuid)
        data = [v.to_dict() for v in s.execute()]
        return Response(status=200, data=data)

    def create(self, request, *args, **kwargs):
        es = Elasticsearch(settings.ES_CLUSTER)
        idx_obj, uuid = self.get_index_and_uuid(**kwargs)
        o = idx_obj(
            user_id=request.data['user_id'],
            page_id=request.data['page_id'],
            subscription_uuid=request.data['subscription_uuid'],
            start=request.data['start'],
            end=request.data['end'],
            created=timezone.now(),
            modified=timezone.now(),
            status=request.data['status']
        )
        o.save(using=es)
        return Response(status=201, data=o.to_dict())

    def update(self, request, *args, **kwargs):
        es = Elasticsearch(settings.ES_CLUSTER)
        idx_obj, uuid = self.get_index_and_uuid(**kwargs)
        o = idx_obj.search(using=es).query('match', subscription_uuid=uuid).query('match', user_id=kwargs['pk']).execute()[0]
        o.update(
            page_id=request.data['page_id'],
            subscription_uuid=request.data['subscription_uuid'],
            start=request.data['start'],
            end=request.data['end'],
            modified=timezone.now(),
            status=request.data['status'],
            using=es
        )
        return Response(status=200, data=o.to_dict())

    def destroy(self, request, *args, **kwargs):
        es = Elasticsearch(settings.ES_CLUSTER)
        idx_obj, uuid = self.get_index_and_uuid(**kwargs)
        s = idx_obj.search(using=es).query('match', subscription_uuid=uuid).query('match', user_id=kwargs['pk'])
        s.delete()
        return Response(status=204)
