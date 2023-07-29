from typing import List

from core.entity import Entity


class System(object):
  def __init__(self) -> None: pass
  def update(self, entities: List[Entity]): pass