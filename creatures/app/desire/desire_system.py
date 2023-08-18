
from typing import List
from .desire_abstract import DesireComponent
from creatures.core.entity import Entity
from creatures.core.system import System


class DesireSystem(System):
  def __init__(self, world) -> None:
    super().__init__(world)

  def update(self, entities: List[Entity]):
    for entity in entities:
      component: DesireComponent = entity.get_component(DesireComponent)
      component.desire.run()