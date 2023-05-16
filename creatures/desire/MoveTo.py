from argparse import Action
from typing import Any, Dict
from creatures.action.action import ActionComponent, Move
from creatures.desire.desire_abstract import Desire
from creatures.entity import Entity
from creatures.location.location import Location
from creatures.primitives import Vector
from creatures.world import World


class MoveTo(Desire):
  def __init__(self, entity: Entity, location: Location, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity)
    self.location = location
    self.never_satisfied = never_satisfied
    self.world = world
  
  def run(self):
    direction = Vector.from_points(self.entity.movement.position, self.location.get()).unit()
    
    if not ActionComponent.__name__ in self.entity.components:
      action_component = ActionComponent()
      self.entity.add_component(action_component)
    else:
      action_component = self.entity.components[ActionComponent.__name__][0]
    
    action_component.action = Move(self.entity, direction)

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
