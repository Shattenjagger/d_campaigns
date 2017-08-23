from rest_framework import serializers
from campaigns.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id',
            'name',
            'description',
            'start',
            'end',
            'recurrence',
            'active',
            'created',
            'modified'
        ]
