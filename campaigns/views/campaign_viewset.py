from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class CampaignViewSet(
    viewsets.ModelViewSet
):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Campaign.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def activate(self, request, *args, **kwargs):
        o = self.get_object()
        s = self.serializer_class
        return Response(s(o).data)

    def deactivate(self, request, *args, **kwargs):
        o = self.get_object()
        s = self.serializer_class
        return Response(s(o).data)
