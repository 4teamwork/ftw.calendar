from ftw.upgrade import UpgradeStep


class FixFullcalendarJsMinification(UpgradeStep):
    """Fix fullcalendar js minification
    """

    def __call__(self):
        self.install_upgrade_profile()
