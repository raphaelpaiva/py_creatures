from typing import List

from creatures.entity import Entity


class System(object):
  def __init__(self) -> None: pass
  def accept(self, entities: List[Entity]): pass
  def update(self): pass