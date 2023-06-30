from argparse import Action
from typing import Any, Dict
from core.action.action import ActionComponent, Move
from core.desire.desire_abstract import Desire
from core.entity import Entity
from core.location.location import Location
from core.primitives import Vector
from core.world import World


class MoveTo(Desire):
  def __init__(self, entity: Entity, location: Location, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity)
    self.location = location
    self.never_satisfied = never_satisfied
    self.world = world
  
  def run(self):
    direction = Vector.from_points(self.entity.movement.position, self.location.get()).unit()
    action_component = self.entity.get_component(ActionComponent)
    
    if not action_component:
      action_component = ActionComponent()
      self.entity.add_component(action_component)
    
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