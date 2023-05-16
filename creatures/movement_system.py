from typing import Iterable, List
from creatures.component import MovementComponent
from creatures.entity import Entity
from creatures.system import System
from creatures.world import World

class MovementSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.processing_list: List[Entity] = []
    self.world: World = world
  
  def update(self, entities: List[Entity]):

    for entity in entities:
      entity.movement.position += entity.movement.velocity * self.world.dt