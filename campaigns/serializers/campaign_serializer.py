from rest_framework import serializers
from campaigns.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)
    rule = serializers.CharField()

    class Meta:
        model = Campaign
        lookup_field = 'uuid'
        fields = [
            'id',
            'name',
            'description',
            'start',
            'end',
            'rule',
            'active',
            'created',
            'modified'
        ]
