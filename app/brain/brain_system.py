from typing import List, Set

from app.brain.brain_component import BrainComponent
from app.creatures.creature import Creature
from app.desire import Wander
from app.desire.MoveTo import MoveTo
from app.desire.desire_abstract import DesireComponent
from core.entity import Entity
from app.location.location import Location
from app.sensor.sensor_component import SensorComponent
from core.system import System
from core.world import World


class BrainSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
        brain_component: BrainComponent = entity.get_component(BrainComponent)
        if brain_component:
          creature = brain_component.creature
          if creature.wandering:
            detected_entities = creature.detected
            if detected_entities:
              target = self.choose_target(brain_component, detected_entities)
              self.follow(creature, target)
          if creature.hungry:
            if creature.following:
              # TODO: Fix this mess
              if creature.target and creature.target.distance(creature.position) <= creature.properties.get('grab_radius', 0):
                creature.target.mark_remove()
                creature.energy.current += 50
                self.wander(creature) # TODO: there should be a desire/behavior stack

  def wander(self, creature: Creature):
    creature.desire = Wander(None, world=self.world) # TODO: Movement System should restrict bounds, not Desire.
  def follow(self, creature: Creature, target: Entity):
    if target:
      creature.desire = MoveTo(creature.entity, Location(target, identifier=target.id), world=self.world)
  
  def choose_target(self, brain: BrainComponent, detected_entities: Set[Entity]) -> Entity:
    if brain.hungry:  
      return self.nearest_edible(brain, detected_entities)

  def nearest_edible(self, brain: BrainComponent, detected_entities: Set[Entity]) -> Entity | None:
      edibles = sorted(
        list(
          filter(
            lambda e: brain.is_edible(e), detected_entities)
          ),
        key=lambda x: x.distance(brain.creature.entity)
      )
      return edibles[0] if edibles else None

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
  
