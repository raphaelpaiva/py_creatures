
from typing import List
from creatures.behavior_abstract import BehaviorComponent
from creatures.entity import Entity
from creatures.system import System

class BehaviorSystem(System):
  def __init__(self) -> None:
    super().__init__()
    self.processing_list: List[Entity] = []
  
  def accept(self, entities: List[Entity]):
    self.processing_list.extend(entities)

  def update(self):
    for entity in self.processing_list:
      for component in entity.components:
        if isinstance(component, BehaviorComponent):
          component.behavior.run()