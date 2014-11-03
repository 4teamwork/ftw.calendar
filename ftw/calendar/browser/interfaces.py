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
