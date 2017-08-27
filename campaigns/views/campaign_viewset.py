from redbeat import RedBeatSchedulerEntry
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class CampaignViewSet(
    viewsets.ModelViewSet
):
    lookup_field = 'uuid'
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Campaign.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # TODO: Perform schedule update on save
    # def perform_update(self, serializer):
    #     pass

    # TODO: Perform schedule remove on destroy
    # def perform_destroy(self, instance):
    #     pass

    def activate(self, request, *args, **kwargs):
        o = self.get_object()
        o.active = True
        o.save(update_fields=['active', ])

        # TODO: Insert schedule into Redis
        # from d_campaigns import celery_app
        # from campaigns.rrule import rrule
        #
        # if o.recurrence.rrules is not None and len(o.recurrence.rrules) > 0:
        #     r = o.recurrence.rrules[0]
        #     schedule = rrule(r)
        #     entry = RedBeatSchedulerEntry(
        #         'task-%s' % o.id, 'campaigns.tasks.add',
        #         schedule,
        #         args=[1, 2],
        #         app=celery_app
        #     )
        #     entry.save()

        s = self.serializer_class
        return Response(s(o).data)

    def deactivate(self, request, *args, **kwargs):
        o = self.get_object()
        o.active = False
        o.save(update_fields=['active', ])

        # TODO: Delete schedule from Redis

        s = self.serializer_class
        return Response(s(o).data)
