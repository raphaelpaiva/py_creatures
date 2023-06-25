from pygame import Surface
from core.component.component import Component
from core.creatures.creature import Creature


class CreatureGraphicComponent(Component):
  def __init__(self, creature: Creature) -> None:
    super().__init__()
    self.creature = creature
  
  def bottom_layer(self): pass

