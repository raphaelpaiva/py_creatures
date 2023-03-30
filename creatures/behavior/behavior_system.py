
from typing import List
from .behavior_abstract import BehaviorComponent
from creatures.entity import Entity
from creatures.system import System

class BehaviorSystem(System):
  def __init__(self) -> None:
    super().__init__()

  def update(self, entities: List[Entity]):
    for entity in entities:
      for component in entity.components.get(BehaviorComponent.__name__, []):
        component.behavior.run()