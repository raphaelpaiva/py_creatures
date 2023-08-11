import logging
from typing import List, Set

from creatures.app.brain.brain_component import BrainComponent
from creatures.app.creatures.creature import Creature
from creatures.app.desire import Wander
from creatures.app.desire.MoveTo import MoveTo
from creatures.app.desire.desire_abstract import DesireComponent, Desire
from creatures.app.desire import Grab, MoveAway
from creatures.core.entity import Entity
from creatures.app.location.location import Location
from creatures.app.sensor.sensor_component import SensorComponent
from creatures.core.system import System
from creatures.core.world import World


class BrainSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__(world)
    self.log = logging.getLogger(self.__class__.__name__)
    self.world = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      brain_component: BrainComponent = entity.get_component(BrainComponent)
      if brain_component:
        creature = brain_component.creature
        brain_component.input_neurons = {
          'hunger': 1 - creature.energy.ratio,
          'detected_entity': 1.0 if creature.detected else 0.0,
          'detected_food': 1.0 if brain_component.detected_edibles else 0.0,
          'detected_predator': 1.0 if brain_component.detected_predators else 0.0,
          'entity_in_grab_range': 1.0 if brain_component.detected_in_grab_range else 0.0,
          'food_in_grab_range': 1.0 if brain_component.food_in_grab_range else 0.0
        }

        default_desire = Wander(creature.entity, world=self.world)
        desire_candidates: List[Desire] = []
        hunger = brain_component.input_neurons['hunger'] > brain_component.hunger_threshold
        detected_food = brain_component.input_neurons['detected_food']
        detected_predator = brain_component.input_neurons['detected_predator']
        entity_in_grab_range = brain_component.input_neurons['entity_in_grab_range']
        food_in_grab_range = brain_component.input_neurons['food_in_grab_range']

        if creature.desire.__class__.__name__ != default_desire.__class__.__name__:
          if creature.desire.satisfied():
            self.log.info(f"Creature {creature.metadata.name} satisfied its desire to {str(creature.desire).lower()}.")
            creature.desire = default_desire
            self.log.info(f"Creature {creature.metadata.name} decided to {str(creature.desire).lower()}.")
        else:
          if hunger and (food_in_grab_range or detected_food):
            food_in_grab_range = brain_component.food_in_grab_range
            target = food_in_grab_range[0] if food_in_grab_range else brain_component.detected_edibles[0]
            desire_candidates.append(Grab(creature.entity, target, self.world))
          if detected_predator:
            desire_candidates.append(MoveAway(creature.entity, brain_component.detected_predators))

        if desire_candidates:
          creature.desire = desire_candidates[0]
          self.log.info(f"Creature {creature.metadata.name} decided to {str(creature.desire).lower()}.")

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
  
