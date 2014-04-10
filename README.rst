Introduction
============

``ftw.calendar`` is a calendar view based on fullcalendar (http://arshaw.com/fullcalendar).


Special requirements
====================
Currently it depends on plone.app.event 1.1b1.
Since all newer versions need plone.app.widgets.
But 1.1b1 has a install bug. You first need to run the plone.app.registry
import step manually, then the full setup. This package fixes this bug
with custom setuphandler, which installs plone.app.event the right way.
Simply import `ftw.calendar with plone.app.event support` profile.

Since plone.app.event supports only plone >= 4.3.
We drop the support for all older plone versions.

Other plone.app.event versions may work or not.

Features
========

- Generic: ftw.calendar doesn't care about the event objects, it only needs
  a collection in which the resulting brains have a start and a end attribute.
  If the calendar view is on an other content type than a collection, it will
  show all events (types defined in portal_calendar) below this context.

- Internationalized: currently ftw.calendar is available
  in german, english and czech. Feel free to add more translations.

- Integrated: ftw.calendar cares about your calendar settings.
  First day of the week is respected and displayed accordingly.

<<<<<<< b937e35635807df49087460f41adee8a08585cc5
- Flexible: The calendar source is implemented as an adapter. Override it to modify
  the title or add css classes.
=======
- CSS Class generator adapter. This allows you to dynamically extend the css
  class on a event item.
>>>>>>> Add css klass generator adapter.

Usage
=====

- Add ``ftw.calendar`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.calendar

- Install the generic import profile.


Use the ``ftwcalendar_view`` as the new default view on any collection.
The default events-collection in a new plone site should work well,
you probably should remove the date criterions though,
since fullcalendar needs to be able to set them according to the selected month.

Calendar Source
===============

For easy customization i recommend extending from the default calendar source
implementation and override one of the three defined functions.

This is an example from `ftw.meeting`:

::

    from ftw.calendar.browser.calendarupdateview import CalendarJSONSource

    class MeetingCalendarJSONSource(CalendarJSONSource):

        def generate_source_dict_from_brain(self, brain):
            output = super(MeetingCalendarJSONSource,
                           self).generate_source_dict_from_brain(brain)

            if brain.Type == 'Meeting' and \
               self.memberid in brain.getAttendeesOrUsers:

                output['className'] += ' attendee'

            return output

`configure.zcml`:

::

    <configure zcml:condition="installed ftw.calendar">
        <adapter
            for="* ftw.meeting.interfaces.IMeetingLayer"
            name="ftw_calendar_source"
            provides="ftw.calendar.browser.interfaces.IFtwCalendarJSONSourceProvider"
            factory=".calendarsource.MeetingCalendarJSONSource"
            />
    </configure>


Troubleshooting
===============

Often there are javascript-errors just after installing and trying the calendar view.
Normally these are due to javascript caching and can be easily solved
by enabling javascript debugging in the js_registry.

Credits
=======

Many thanks to Adam Shaw for jq.fullcalendar.


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.3`,.


Links
=====

- Github: https://github.com/4teamwork/ftw.calendar
- Issues: https://github.com/4teamwork/ftw.calendar/issues
- Pypi: http://pypi.python.org/pypi/ftw.calendar
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.calendar


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.calendar`` is licensed under GNU General Public License, version 2.
