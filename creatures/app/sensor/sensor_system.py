from typing import List
from creatures.core.entity import Entity
from creatures.app.sensor.sensor_component import SensorComponent
from creatures.core.system import System


class SensorSystem(System):
  def __init__(self, world) -> None:
    super().__init__(world)

  def update(self, entities: List[Entity]):
    for entity in entities:
      sensor_component: SensorComponent = entity.get_component(SensorComponent)
      if sensor_component:
        sensor_component.detected = set()
        for sensor in sensor_component.sensors:
          sensor.position = entity.movement.position
          sensor_component.detected = sensor_component.detected.union(sensor.scan(entities))
          sensor_component.detected.remove(entity)