from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class EventBuilder(ArchetypesBuilder):

    portal_type = 'Event'

builder_registry.register('event', EventBuilder)
