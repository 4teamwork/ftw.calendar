from zope.interface import Interface


class IFtwCalendarLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IFtwCalendarJSONSourceProvider(Interface):
    """ Provides the JSON source to fill the calendar with events.
    """

    def generate_json_calendar_source():
        """ Calls the following methods to get the calendar source and returns
            is as JSON.
        """

    def get_event_brains():
        """ Returns list of brains to display in the current calendar view.
        """

    def generate_source_dict_from_brain(brain):
        """ Reads the relevant information from the brain and generates a dict
            based on thos informations. This dict is later converted to JSON.
        """


class IFtwCalendarEventCreator(Interface):

    def getEventType():
        """ Get the calendar event type name to be adden when
            user clicks in calendar.

        @return: event type as string
        """

    def createEvent(title, start_date):
        """ Creates a calendar event in the given context and data.

        @return: the newly created event
        """
