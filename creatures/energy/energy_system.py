from typing import List
from creatures.action.action import Action, ActionComponent
from creatures.component.component import EnergyComponent
from creatures.entity import Entity
from creatures.primitives import Vector
from creatures.system import System
from creatures.component.component import EnergyComponent
from creatures.world import World

class EnergySystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      energy_component = entity.get_component(EnergyComponent)
      if energy_component:
        energy_component.current -= energy_component.rate * self.world.dt
        energy_component.current = max(0, energy_component.current)

        if energy_component.current <= 0:
          entity.movement.velocity = Vector(0,0)