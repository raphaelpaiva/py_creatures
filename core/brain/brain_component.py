from __future__ import annotations
from typing import TYPE_CHECKING
from core.component.component import Component


if TYPE_CHECKING:
  from core.creatures.creature import Creature
  
class BrainComponent(Component):
  def __init__(self, creature: Creature) -> None:
    super().__init__()
    self.creature: Creature = creature