import uuid

from django.conf import settings
from django.db import models
from recurrence import deserialize
from recurrence import serialize
from recurrence.fields import RecurrenceField


class CustomAction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    recurrence = RecurrenceField()

    def get_rule(self):
        if self.recurrence.rrules is not None:
            if len(self.recurrence.rrules) > 0:
                return serialize(self.recurrence.rrules[0])
        return None

    def set_rule(self, i):
        self.recurrence = deserialize(i)

    rule = property(get_rule, set_rule)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
