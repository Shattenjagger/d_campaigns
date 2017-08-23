import json

import celery
import recurrence
from django.test import TestCase
from django.utils import timezone
from recurrence import serialize
from redbeat import RedBeatSchedulerEntry
from redbeat.decoder import RedBeatJSONEncoder

from campaigns.rrule import rrule


class RRulesRedBeatSchedulerEntryTests(TestCase):
    def test_rrules(self):
        r_rule = recurrence.Rule(
            recurrence.SECONDLY, 5
        )
        print(serialize(r_rule))

        from d_campaigns import celery_app
        interval = celery.schedules.schedule(run_every=5)

        # entry = RedBeatSchedulerEntry('task-name-2', 'campaigns.tasks.add', serialize(r_rule), args=[5, 2], app=celery_app)

        r = rrule(freq=r_rule.freq)
        r.rrule = r_rule.to_dateutil_rrule()

        print(r)

        entry = RedBeatSchedulerEntry('task-name-3', 'campaigns.tasks.add', r, args=[12, 2], app=celery_app)
        entry.save()

