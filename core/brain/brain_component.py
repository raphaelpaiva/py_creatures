from __future__ import annotations
from typing import TYPE_CHECKING
from core.component.component import Component


if TYPE_CHECKING:
  from core.creatures.creature import Creature
  
class BrainComponent(Component):
  def __init__(self, creature: Creature, hunger_threshold: float = 50.0) -> None:
    super().__init__()
    self.creature: Creature = creature
    self.hunger_threshold   = hunger_threshold
  
  @property
  def hungry(self) -> bool:
    return self.creature.energy.current < self.hunger_threshold