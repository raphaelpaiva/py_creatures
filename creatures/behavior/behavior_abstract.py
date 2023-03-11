from abc import abstractmethod
from creatures.component import Component

from creatures.entity import Entity

class Behavior(object):
  def __init__(self, entity: Entity=None) -> None:
    super().__init__()
    self.entity = entity

  @property
  def type(self) -> str:
    return self.__class__.__name__

  @abstractmethod
  def run(self, world = None) -> None: pass
  
  @abstractmethod
  def satisfied(self): pass
  
  @abstractmethod
  def to_dict(self): pass
  
  @property
  def entity(self):
    return self._entity
  
  @entity.setter
  def entity(self, other: Entity):
    self._entity = other

  def __str__(self) -> str:
    return self.type

class BehaviorComponent(Component):
  def __init__(self, behavior: Behavior) -> None:
    super().__init__()
    self.behavior = behavior