from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder.dexterity import DexterityBuilder
from Products.CMFPlone.utils import getFSVersionTuple


class EventBuilderMixin(object):
    portal_type = 'Event'


class ATEventBuilder(EventBuilderMixin, ArchetypesBuilder):
    pass


class DXEventBuilder(EventBuilderMixin, DexterityBuilder):
    pass


if getFSVersionTuple() > (5, ):
    builder_registry.register('event', DXEventBuilder)
else:
    builder_registry.register('event', ATEventBuilder)
