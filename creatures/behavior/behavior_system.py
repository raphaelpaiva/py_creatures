
from typing import List
from .behavior_abstract import BehaviorComponent
from creatures.entity import Entity
from creatures.system import System

class BehaviorSystem(System):
  def __init__(self) -> None:
    super().__init__()
    self.processing_list: List[Entity] = []
  
  def accept(self, entities: List[Entity]):
    self.processing_list = entities

  def update(self):
    for entity in self.processing_list:
      for component in entity.components.get(BehaviorComponent.__name__, []):
        component.behavior.run()