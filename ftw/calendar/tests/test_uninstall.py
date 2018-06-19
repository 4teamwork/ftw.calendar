from ftw.testing.genericsetup import GenericSetupUninstallMixin
from ftw.testing.genericsetup import apply_generic_setup_layer
from unittest2 import TestCase


@apply_generic_setup_layer
class TestGenericSetupUninstall(TestCase, GenericSetupUninstallMixin):
    package = 'ftw.calendar'
    install_dependencies = False

    def _install_package(self):
        self.setup_tool.runAllImportStepsFromProfile(
            'profile-ftw.calendar:general', ignore_dependencies=True)
        self.setup_tool.runAllImportStepsFromProfile(
            'profile-ftw.calendar:default', ignore_dependencies=True)
