from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from campaigns.models import CustomAction
from campaigns.serializers import CustomActionSerializer


class CustomActionViewSet(
    viewsets.ModelViewSet
):
    lookup_field = 'uuid'
    serializer_class = CustomActionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return CustomAction.objects.filter(owner=user)

    def perform_create(self, serializer):
        # TODO: Perform schedule insert on save
        serializer.save(owner=self.request.user)

    # TODO: Perform schedule update on save
    # def perform_update(self, serializer):
    #     pass

    # TODO: Perform schedule remove on destroy
    # def perform_destroy(self, instance):
    #     pass
