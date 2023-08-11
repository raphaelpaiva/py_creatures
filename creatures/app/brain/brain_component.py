from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Set, Iterable, List
from creatures.core.component.component import Component
from creatures.core.entity import Entity
from .reasoners.diet import DietReasoner
from .reasoners.diet import HerbivoreDietReasoner


if TYPE_CHECKING:
  from creatures.app.creatures.creature import Creature


class BrainComponent(Component):
  def __init__(
    self,
    creature: Creature,
    hunger_threshold: float = 0.5,
    diet_reasoner: DietReasoner = None) -> None:
    super().__init__()
    self.creature: Creature = creature
    self.hunger_threshold = hunger_threshold
    self.diet_reasoner: DietReasoner = diet_reasoner if diet_reasoner else HerbivoreDietReasoner()
    self.input_neurons: Dict[str, float] = {
      'hunger': 0.0,
      'detected_entity': 0.0,
      'detected_food': 0.0,
      'detected_predator': 0.0,
      'entity_in_grab_range': 0.0,
      'food_in_grab_range': 0.0
    }

  def is_edible(self, entity: Entity) -> bool:
    return self.diet_reasoner.is_edible(entity)

  def is_predator(self, entity: Entity) -> bool:
    return self.creature.is_herbivore and entity.type.lower() == 'creature'

  @property
  def hungry(self) -> bool:
    return self.creature.energy.current < self.hunger_threshold

  @property
  def detected(self) -> Set[Entity]:
    return self.creature.sensor_component.detected

  @property
  def detected_edibles(self) -> Iterable[Entity]:
    return sorted(list(filter(self.is_edible, self.detected)), key=self.creature.distance)

  @property
  def detected_predators(self) -> Iterable[Entity]:
    return list(filter(self.is_predator, self.detected))

  @property
  def detected_in_grab_range(self) -> Iterable[Entity]:
    return list(filter(self.creature.in_grab_range, self.detected))

  @property
  def food_in_grab_range(self) -> List[Entity]:
    return sorted(list(filter(self.creature.in_grab_range, self.detected_edibles)), key=self.creature.distance)
