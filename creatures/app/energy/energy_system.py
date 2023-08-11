import logging
from typing import List
from creatures.core.entity import Entity
from creatures.core.primitives import Vector
from creatures.core.system import System
from creatures.core.component.component import EnergyComponent
from creatures.core.world import World


class EnergySystem(System):
  def __init__(self, world: World) -> None:
    super().__init__(world)
    self.log = logging.getLogger(EnergySystem.__name__)
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      energy_component: EnergyComponent = entity.get_component(EnergyComponent)
      if energy_component:
        energy_component.current -= energy_component.rate * self.world.dt
        energy_component.current = max(0.0, energy_component.current)
        self.log.debug(f"{entity.name}: {energy_component.current} | {energy_component.rate} * {self.world.dt} = {energy_component.rate * self.world.dt}")

        if energy_component.current <= 0:
          entity.movement.velocity = Vector(0,0)
          entity.mark_remove()
