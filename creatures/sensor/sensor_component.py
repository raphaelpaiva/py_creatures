from typing import Any, Dict, List, Set
from creatures.component.component import Component
from creatures.entity import Entity
from creatures.sensor.sensor import RadialSensor, Sensor


class SensorComponent(Component):
  def __init__(self, sensors: List[Sensor]) -> None:
    super().__init__()
    self.detected: Set[Entity] = set()
    self.sensors: Sensor = sensors if sensors else []
  
  def radial_sensors(self) -> List[RadialSensor]:
    return list(filter(lambda s: isinstance(s, RadialSensor), self.sensors))
  
  def max_radius(self):
    return max(self.radial_sensors(), key=lambda s: s.radius).radius

  def to_dict(self) -> Dict[str, Any]:
    return {
      'sensors': [s.to_dict() for s in self.sensors],
      'detected': [e.id for e in list(self.detected)]
    }