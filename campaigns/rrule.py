import celery
from recurrence import Recurrence
from recurrence import serialize

try:  # celery 4.x
    from celery.schedules import BaseSchedule as schedule
except ImportError:  # celery 3.x
    from celery.schedules import schedule

# TODO: Implement proper schedule based on Recurrence Rule
#
# class rrule(schedule):
#
#     def __init__(self, rule, dtstart, until, **kwargs):
#         super(rrule, self).__init__(**kwargs)
#
#         self.rule = rule
#
#         dtstart = self.maybe_make_aware(dtstart) if dtstart else \
#             self.maybe_make_aware(self.now())
#         until = self.maybe_make_aware(until) if until else None
#
#         self.dtstart = dtstart
#         self.until = until
#
#     def remaining_estimate(self, last_run_at):
#         last_run_at = self.maybe_make_aware(last_run_at)
#         r = Recurrence(rrules=[self.rule, ])
#         g = r.occurrences(last_run_at, self.until)
#         # print(list(g))
#         i = g.__iter__()
#         next_run = next(i)
#         print("======")
#         print(next_run)
#         next_run = next(i)
#         print("======")
#         print(next_run)
#         if next_run:
#             next_run = self.maybe_make_aware(next_run)
#             now = self.maybe_make_aware(self.now())
#             delta = next_run - now
#             return delta
#         return None
#
#     def is_due(self, last_run_at):
#         rem_delta = self.remaining_estimate(last_run_at)
#         if rem_delta is not None:
#             rem = max(rem_delta.total_seconds(), 0)
#             due = rem == 0
#             if due:
#                 rem_delta = self.remaining_estimate(self.now())
#                 if rem_delta is not None:
#                     rem = max(rem_delta.total_seconds(), 0)
#                 else:
#                     rem = None
#             return celery.schedules.schedstate(due, rem)
#         return celery.schedules.schedstate(False, None)
#
#     def __repr__(self):
#         return serialize(self.rule)
#
