from rest_framework import serializers
from campaigns.models import CustomAction


class CustomActionSerializer(serializers.ModelSerializer):
    rule = serializers.CharField()

    class Meta:
        model = CustomAction
        fields = [
            'id',
            'name',
            'description',
            'rule',
            'created',
            'modified'
        ]
