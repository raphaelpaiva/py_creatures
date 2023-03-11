from typing import Any, Dict
from creatures.behavior.behavior_abstract import Behavior
from creatures.entity import Entity


class StayStill(Behavior):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
  
  def satisfied(self):
    return True
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id
    }
