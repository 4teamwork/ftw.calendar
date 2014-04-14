from zope.interface import Interface


class IFtwCalendarLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IEventCssKlassGenerator(Interface):
    """Returns css klasses for Event Items in the ftwfullcalendar view. """

    def __init__(item, request):
        """Adapts item and request"""

    def generate_css_klasses():
        """ returns a string with css klasses."""
