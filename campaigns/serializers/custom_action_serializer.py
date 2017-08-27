from rest_framework import serializers
from campaigns.models import CustomAction


class CustomActionSerializer(serializers.ModelSerializer):
    rule = serializers.CharField()

    class Meta:
        model = CustomAction
        lookup_field = 'uuid'
        fields = [
            'id',
            'name',
            'description',
            'rule',
            'created',
            'modified'
        ]
