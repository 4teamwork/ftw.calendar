from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry


class AtEventBuilder(ArchetypesBuilder):
    portal_type = 'Event'


builder_registry.register('at event', AtEventBuilder)
