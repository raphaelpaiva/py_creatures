from typing import List

from pygame import init
from core.brain.brain_component import BrainComponent
from core.component.component import EnergyComponent
from core.desire import Wander
from core.desire.desire_abstract import DesireComponent
from core.entity import Entity
from core.sensor.sensor_component import SensorComponent
from core.system import System

class BrainSystem(System):
  def __init__(self) -> None:
    super().__init__()
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      brain_component = entity.get_component(BrainComponent)
      if brain_component:
        cons = Consciousness(entity)
        if cons.wandering:
          if cons.entities_nearby:
            cons.follow(cons.target)


        if hungry(entity):
          desire_component: DesireComponent = entity.get_component(DesireComponent)
          
          #desire_component.desire = SearchForFood(entity)

def hungry(entity: Entity) -> bool:
  energy_component: EnergyComponent = entity.get_component(EnergyComponent)
  if energy_component:
    return energy_component.current < 50.0

  return False

class Consciousness(object):
  def __init__(self, entity: Entity) -> None:
    self.entity = entity
    self.entities_nearby = self.detected()
    self.target = self.entities_nearby[0] if self.entities_nearby else None
  
  @property
  def wandering(self) -> bool:
    desire_component: DesireComponent = self.entity.get_component(DesireComponent)
    return desire_component and isinstance(desire_component.desire, Wander)

  def detected(self) -> List[Entity]:
    sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
    if sensor_component and sensor_component.detected:
      return list(sensor_component.detected)
    else:
      return []
