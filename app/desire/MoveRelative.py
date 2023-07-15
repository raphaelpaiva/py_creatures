from app.desire.MoveTo import MoveTo
from core.entity import Entity
from core.primitives import Vector
from core.world import World
from app.location import Location


class MoveRelative(MoveTo):
  def __init__(self, entity: Entity, location: Vector, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity, Location(location), never_satisfied, world)
  
  def run(self, world: World = None):
    self.entity.movement.velocity += self.location.get().scalar(self.entity.properties.get('speed', 1.0))
  
  def satisfied(self):
    return not self.never_satisfied
