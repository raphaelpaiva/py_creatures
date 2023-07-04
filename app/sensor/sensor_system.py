from typing import List
from core.entity import Entity
from app.sensor.sensor_component import SensorComponent
from core.system import System


class SensorSystem(System):
  def __init__(self) -> None:
    super().__init__()

  def update(self, entities: List[Entity]):
    for entity in entities:
      sensor_component: SensorComponent = entity.get_component(SensorComponent)
      if sensor_component:
        sensor_component.detected = set()
        for sensor in sensor_component.sensors:
          sensor.position = entity.movement.position
          sensor_component.detected = sensor_component.detected.union(sensor.scan(entities))
          sensor_component.detected.remove(entity)