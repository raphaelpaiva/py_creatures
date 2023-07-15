from typing import Iterable, Dict, Any
from core.entity import Entity
from core.primitives import Vector
from app.sensor import SensorComponent
from app.action import ActionComponent, Move
from .desire_abstract import Desire



class MoveAway(Desire):
  def __init__(self, entity: Entity, from_entities: Entity | Iterable[Entity]):
    super().__init__(entity)
    self.from_entities = [from_entities] if isinstance(from_entities, Entity) else from_entities

  def run(self, world=None) -> None:
    direction = Vector(0,0)
    for other in self.from_entities:
      direction = (direction + Vector.from_points(other.movement.position, self.entity.movement.position)).unit()

    action_component = self.entity.get_component(ActionComponent)
    if not action_component:
      action_component = ActionComponent()
      self.entity.add_component(action_component)

    action_component.action = Move(self.entity, direction)

  def satisfied(self):
    sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
    if not sensor_component:
      return True

    return len(sensor_component.detected.intersection(self.from_entities)) == 0

  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "from_entities": [e.id for e in self.from_entities]
    }

  def __str__(self):
    return f"move away from {', '.join([e.name for e in self.from_entities])}"
