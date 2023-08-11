from .diet_reasoner import DietReasoner
from creatures.core.entity import Entity


class HerbivoreDietReasoner(DietReasoner):
  def __init__(self):
    super().__init__()

  def is_edible(self, entity: Entity):
    return entity.is_resource
