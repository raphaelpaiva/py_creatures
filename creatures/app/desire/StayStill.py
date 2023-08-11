from typing import Any, Dict
from creatures.app.desire.desire_abstract import Desire
from creatures.core.entity import Entity


class StayStill(Desire):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
  
  def satisfied(self):
    return True
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id
    }
