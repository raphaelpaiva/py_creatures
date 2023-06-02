from typing import List
from creatures.action.action import Action, ActionComponent
from creatures.component.component import EnergyComponent
from creatures.entity import Entity
from creatures.system import System
from creatures.component.component import EnergyComponent
from creatures.world import World

class EnergySystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      for energy_component in entity.components.get(EnergyComponent.__name__, []):
        energy_component.current -= energy_component.rate * self.world.dt
        energy_component.current = max(0, energy_component.current)
      for action_component in entity.components.get(ActionComponent.__name__, []):
        action: Action = action_component.action if action_component else None
        if action:
          energy_component.current -= action.energy_cost