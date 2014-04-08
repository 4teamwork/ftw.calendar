from Products.CMFCore.utils import getToolByName


def install_p_a_event(portal):
    setup = getToolByName(portal, 'portal_setup')

    profileid = 'profile-plone.app.event:default'
    setup.runImportStepFromProfile(profileid,
                                   'plone.app.registry',
                                   run_dependencies=False,
                                   purge_old=False)


def setup_misc(context):
    if context.readDataFile('ftw.calendar_various.txt') is None:
        return

    portal = context.getSite()
    install_p_a_event(portal)
