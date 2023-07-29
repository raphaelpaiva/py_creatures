from typing import List

from core.entity import Entity


class System(object):
  def __init__(self, world) -> None:
    self.world = world

  def update(self, entities: List[Entity]): pass
