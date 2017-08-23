from redbeat import RedBeatSchedulerEntry


class RRulesRedBeatSchedulerEntry(RedBeatSchedulerEntry):
    def __init__(self, name=None, task=None,
                 args=None, kwargs=None, enabled=True, **clsargs):
        schedule = None
        super(RRulesRedBeatSchedulerEntry, self).__init__(
            name=name,
            task=task,
            schedule=schedule,
            args=args,
            kwargs=kwargs,
            enabled=enabled,
            **clsargs
        )
