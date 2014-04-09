from Products.CMFCore.utils import getToolByName


def install_p_a_event(portal):
    setup = getToolByName(portal, 'portal_setup')

    profileid = 'profile-plone.app.event:default'
    setup.runImportStepFromProfile(profileid,
                                   'plone.app.registry',
                                   run_dependencies=False,
                                   purge_old=False)


def set_calendar_types(portal):
    portal_calendar = getToolByName(portal, 'portal_calendar')
    types = list(portal_calendar.calendar_types)
    types.append('plone.app.event.dx.event')
    portal_calendar.calendar_types = tuple(types)


def setup_paevent(context):

    if context.readDataFile('ftw.calendar.paevent_support.txt') is None:
        return

    portal = context.getSite()
    # XXX: It's not possible to install plone.app.event 1.1b1 thru
    # portal_setup without this
    install_p_a_event(portal)
    set_calendar_types(portal)
