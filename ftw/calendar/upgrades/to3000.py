from ftw.calendar import HAS_PAEVENT
from ftw.calendar.setuphandlers import set_calendar_types
from ftw.upgrade import UpgradeStep


class Upgrade(UpgradeStep):
    def __call__(self):
        if HAS_PAEVENT:
            set_calendar_types(self.portal)
