from creatures.desire.MoveTo import MoveTo
from creatures.entity import Entity
from creatures.primitives import Vector
from creatures.world import World

class MoveRelative(MoveTo):
  def __init__(self, entity: Entity, location: Vector, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity, location, never_satisfied, world)
  
  def run(self):
    self.entity.movement.velocity += self.location.get().scalar(self.entity.properties.get('speed', 1.0))
  
  def satisfied(self):
    return not self.never_satisfied
