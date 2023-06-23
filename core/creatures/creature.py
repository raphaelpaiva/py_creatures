from core.component.component import MetaDataComponent, MovementComponent
from core.desire import StayStill
from core.desire.desire_abstract import Desire, DesireComponent
from core.entity import Entity, _next_id
from core.render_system.graphics import SimpleGraphicComponent
from core.sensor.sensor import RadialSensor
from core.sensor.sensor_component import SensorComponent

class Creature(object):
  def __init__(self, id: str) -> None:
    self.entity           = Entity('creature_')
    self.movement         = MovementComponent()
    self.metadata         = MetaDataComponent(self.entity.id, 'creature')
    
    self.entity.add_component(self.metadata)
    
    self.sensor           = RadialSensor(15)
    self._desire          = StayStill(self.entity)
    self.desire_component = DesireComponent(self._desire)
    self.graphics         = SimpleGraphicComponent(self.entity)

    self.entity.add_component(self.movement)
    self.entity.add_component(self.graphics)
    self.entity.add_component(SensorComponent([self.sensor]))
    self.entity.add_component(DesireComponent(self.desire))
    

  @property
  def desire(self):
    return self.desire_component.desire

  @desire.setter
  def desire(self, desire: Desire):
    self.desire_component.desire = desire