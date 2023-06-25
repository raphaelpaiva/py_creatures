from typing import Set
from core.brain.brain_component import BrainComponent
from core.component.component import MetaDataComponent, MovementComponent
from core.desire import StayStill, Wander
from core.desire.desire_abstract import Desire, DesireComponent
from core.entity import Entity
from core.primitives import Vector
from core.render_system.graphics import SimpleGraphicComponent
from core.sensor.sensor import RadialSensor
from core.sensor.sensor_component import SensorComponent

class Creature(object):
  def __init__(self, id: str) -> None:
    self.entity           = Entity('creature_')
    self.movement         = MovementComponent(Vector(100, 100))
    self.metadata         = MetaDataComponent(self.entity.id, 'creature')
    
    self.entity.add_component(self.metadata)
    
    self.sensor           = RadialSensor(50)
    self.sensor_component = SensorComponent([self.sensor])
    self._desire          = StayStill(self.entity)
    self.desire_component = DesireComponent(self._desire)

    self.entity.add_component(self.movement)
    self.entity.add_component(self.sensor_component)
    self.entity.add_component(self.desire_component)
    
    self.graphics         = SimpleGraphicComponent(self.entity)
    self.entity.add_component(self.graphics)
    self.entity.add_component(BrainComponent(self))
  
  @property
  def desire(self) -> Desire:
    return self.desire_component.desire

  @desire.setter
  def desire(self, desire: Desire):
    self.desire_component.desire = desire
  
  @property
  def wandering(self) -> bool:
    return isinstance(self.desire, Wander)
  
  @property
  def detected(self) -> Set[Entity]:
    return self.sensor_component.detected