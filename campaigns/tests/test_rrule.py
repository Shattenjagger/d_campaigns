import recurrence
from django.test import TestCase
from django.utils import timezone

# TODO: Tests are disabled during not implemented conversion
# from campaigns.rrule import rrule
#
#
# class RRuleTests(TestCase):
#     def test_rrules(self):
#         r = recurrence.Rule(
#             recurrence.SECONDLY,
#             interval=5
#         )
#         t = timezone.now()
#         print(t)
#         k = rrule(r, t, None)
#         print(k.remaining_estimate(t))
