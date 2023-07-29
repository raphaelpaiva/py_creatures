from typing import Iterable, List
from core.component.component import MovementComponent
from core.entity import Entity
from core.system import System
from core.world import World


class MovementSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.processing_list: List[Entity] = []
    self.world: World = world
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      entity.movement.position += entity.movement.velocity * self.world.dt
