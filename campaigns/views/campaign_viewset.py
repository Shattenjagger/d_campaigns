from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Campaign.objects.filter(owner=user)
