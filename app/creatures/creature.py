from typing import Any, Dict, Set
from app.brain.brain_component import BrainComponent
from core.component.component import EnergyComponent, MetaDataComponent, MovementComponent
from app.desire import MoveTo, StayStill, Wander
from app.desire.desire_abstract import Desire, DesireComponent
from core.entity import Entity
from core.primitives import Vector
from app.render_system.graphics import SimpleGraphicComponent
from app.sensor.sensor import RadialSensor, Sensor
from app.sensor.sensor_component import SensorComponent
from app.brain.reasoners.diet import HerbivoreDietReasoner, CarnivoreDietReasoner

DIET_REASONERS = {
  'herbivore': HerbivoreDietReasoner,
  'carnivore': CarnivoreDietReasoner
}

class Creature(object):
  def __init__(self,
    id:        str,
    movement:  MovementComponent      = MovementComponent(Vector(100, 100)),
    metadata:  MetaDataComponent      = None,
    brain:     BrainComponent         = BrainComponent(None),
    sensor:    Sensor                 = RadialSensor(50),
    desire:    Desire                 = StayStill(None),
    energy:    EnergyComponent        = EnergyComponent(),
    graphics:  SimpleGraphicComponent = None,
    properties: Dict[str, Any]        = {}) -> None:
    self.entity            = Entity(id, entity_type=self.__class__.__name__)
    self.properties        = properties
    self.entity.properties = properties
    self.movement          = movement
    self.metadata          = metadata if metadata else MetaDataComponent(self.entity.id, self.__class__.__name__)
    self.brain             = brain if brain else BrainComponent(self)

    diet = self.properties.get('diet', 'herbivore')
    self.brain.diet_reasoner = DIET_REASONERS.get(diet)()

    self.entity.add_component(self.metadata)
    
    self.sensor           = sensor
    self.sensor_component = SensorComponent([self.sensor])
    self.desire_component = None # set by desire setter
    self.desire           = desire
    self.energy           = energy

    self.entity.add_component(self.movement)
    self.entity.add_component(self.sensor_component)
    self.entity.add_component(self.desire_component)
    
    self.entity.add_component(self.brain)
    self.entity.add_component(self.energy)
    
    self.graphics = graphics if graphics else SimpleGraphicComponent(self.entity)
    self.entity.add_component(self.graphics)
  
  @property
  def desire(self) -> Desire:
    return self.desire_component.desire

  @desire.setter
  def desire(self, desire: Desire):
    desire.entity = self.entity
    self._desire = desire
    if self.desire_component:
      self.desire_component.desire = desire
    else:
      self.desire_component = DesireComponent(desire)

  @property
  def brain(self) -> BrainComponent:
    return self._brain

  @brain.setter
  def brain(self, brain: BrainComponent):
    brain.creature = self
    self._brain = brain
  
  @property
  def wandering(self) -> bool:
    return isinstance(self.desire, Wander)
  
  @property
  def detected(self) -> Set[Entity]:
    return self.sensor_component.detected
  
  @property
  def hungry(self) -> bool:
    return self.brain.hungry
  
  @property
  def following(self) -> bool:
    return isinstance(self.desire, MoveTo)
  
  @property
  def target(self) -> Entity | None:
    return self.desire.location.target if self.following and isinstance(self.desire.location.target, Entity) else None
  
  @property
  def position(self) -> Vector:
    return self.movement.position