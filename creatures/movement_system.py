from typing import Iterable, List
from creatures.component import MovementComponent
from creatures.entity import Entity
from creatures.system import System

class MovementSystem(System):
  def __init__(self) -> None:
    super().__init__()
    self.processing_list: List[MovementComponent] = []
  
  def accept(self, entities: List[Entity]):
    super().accept(entities)
    self.processing_list.extend([e.components[MovementComponent.__name__] for e in entities])
