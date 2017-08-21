from rest_framework import viewsets

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
