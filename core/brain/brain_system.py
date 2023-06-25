from typing import List

from pygame import init
from core.brain.brain_component import BrainComponent
from core.component.component import EnergyComponent
from core.creatures.creature import Creature
from core.desire import Wander
from core.desire.MoveTo import MoveTo
from core.desire.desire_abstract import DesireComponent
from core.entity import Entity
from core.location.location import Location
from core.sensor.sensor_component import SensorComponent
from core.system import System
from core.world import World

class BrainSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
        brain_component = entity.get_component(BrainComponent)
        if brain_component:
          creature = brain_component.creature
          if creature.wandering:
            detected_entities = creature.detected
            if detected_entities:
              self.follow(creature, list(detected_entities)[0])

          # if hungry(entity):
          #   desire_component: DesireComponent = entity.get_component(DesireComponent)
            
            #desire_component.desire = SearchForFood(entity)
  def follow(self, creature: Creature, target: Entity):
    creature.desire = MoveTo(creature.entity, Location(lambda: target.movement.position), world=self.world)

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
  
  def follow(self, target: Entity):
    self.entity

