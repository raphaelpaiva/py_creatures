from creatures.core.entity import Entity
from .diet_reasoner import DietReasoner


class CarnivoreDietReasoner(DietReasoner):
  def __init__(self):
    super().__init__()

  def is_edible(self, entity: Entity):
    return entity.type.lower() == 'creature'
