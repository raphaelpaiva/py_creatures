
from typing import List
from .desire_abstract import DesireComponent
from creatures.entity import Entity
from creatures.system import System

class DesireSystem(System):
  def __init__(self) -> None:
    super().__init__()

  def update(self, entities: List[Entity]):
    for entity in entities:
      component = entity.get_component(DesireComponent.__name__)
      component.desire.run()