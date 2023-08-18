from typing import List, Set
from creatures.core.component.component import MovementComponent

from creatures.core.entity import Entity
from creatures.core.primitives import Vector


class Sensor(object):
  def __init__(self) -> None:
    self.position = Vector(0,0)

  def scan(self, entities: List[Entity]) -> Set[Entity]: pass

class RadialSensor(Sensor):
  def __init__(self, radius: float = 7.0) -> None:
    super().__init__()
    self.radius = radius
  
  def scan(self, entities: List[Entity]) -> Set[Entity]:
    result: Set[Entity] = set()
    for entity  in entities:
      movement_component = entity.get_component(MovementComponent)
      if movement_component:
        if entity.distance(self.position) <= self.radius:
          result.add(entity)

    return result

  def to_dict(self):
    return {
      'type': 'RadialSensor',
      'position': self.position.to_dict(),
      'radius': self.radius
    }