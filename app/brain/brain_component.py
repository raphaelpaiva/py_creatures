from __future__ import annotations
from typing import TYPE_CHECKING
from core.component.component import Component
from core.entity import Entity
from .reasoners.diet import DietReasoner
from .reasoners.diet import HerbivoreDietReasoner


if TYPE_CHECKING:
  from app.creatures.creature import Creature


class BrainComponent(Component):
  def __init__(
    self,
    creature: Creature,
    hunger_threshold: float = 50.0,
    diet_reasoner: DietReasoner = None) -> None:
    super().__init__()
    self.creature: Creature = creature
    self.hunger_threshold = hunger_threshold
    self.diet_reasoner: DietReasoner = diet_reasoner if diet_reasoner else HerbivoreDietReasoner()

  def is_edible(self, entity: Entity):
    return self.diet_reasoner.is_edible(entity)

  @property
  def hungry(self) -> bool:
    return self.creature.energy.current < self.hunger_threshold
