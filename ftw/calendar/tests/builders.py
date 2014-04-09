from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class AtEventBuilder(ArchetypesBuilder):
    portal_type = 'Event'


builder_registry.register('at event', AtEventBuilder)
