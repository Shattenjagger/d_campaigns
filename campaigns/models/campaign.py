import uuid

from django.db import models
from django.conf import settings
from recurrence.fields import RecurrenceField


class Campaign(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    recurrence = RecurrenceField()

    active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
