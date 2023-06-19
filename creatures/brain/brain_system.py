from typing import List
from creatures.brain.brain_component import BrainComponent
from creatures.component.component import EnergyComponent
from creatures.desire.desire_abstract import DesireComponent
from creatures.entity import Entity
from creatures.system import System


class BrainSystem(System):
  def __init__(self) -> None:
    super().__init__()
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      brain_component = entity.get_component(BrainComponent)
      if brain_component:
        if hungry(entity):
          desire_component: DesireComponent = entity.get_component(DesireComponent)
          
          #desire_component.desire = SearchForFood(entity)

def hungry(entity: Entity) -> bool:
  energy_component: EnergyComponent = entity.get_component(EnergyComponent)
  if energy_component:
    return energy_component.current < 50.0

  return False