import uuid

from django.conf import settings
from django.db import models
from recurrence.fields import RecurrenceField


class Campaign(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    recurrence = RecurrenceField()

    # FIXME: Disabled during lack of original code
    # choice = models.CharField()
    # segment = models.ForeignKey()
    # node = models.ForeignKey()

    active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
