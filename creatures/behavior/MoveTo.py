from typing import Any, Dict
from creatures.behavior.behavior_abstract import Behavior
from creatures.entity import Entity
from creatures.location import Location
from creatures.primitives import Vector
from creatures.world import World


class MoveTo(Behavior):
  def __init__(self, entity: Entity, location: Location, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity)
    self.location = location
    self.never_satisfied = never_satisfied
    self.world = world
  
  def run(self):
    speed = self.entity.properties.get('speed', 1.0)
    direction = Vector.from_points(self.entity.movement.position, self.location.get()).unit()
    self.entity.movement.velocity = direction.scalar(speed)

  def satisfied(self):
    if self.never_satisfied:
      return False
    else:
      return self.entity.movement.position == self.location.get()
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "location": self.location.to_dict(),
      "never_satisfied": self.never_satisfied
    }
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.location})"
