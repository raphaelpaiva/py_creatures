from abc import abstractmethod
from typing import Any, Dict
from core.component.component import Component

from core.entity import Entity


class Desire(object):
  def __init__(self, entity: Entity = None) -> None:
    super().__init__()
    self._entity = entity

  @property
  def type(self) -> str:
    return self.__class__.__name__

  @abstractmethod
  def run(self, world=None) -> None: pass
  
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


class DesireComponent(Component):
  def __init__(self, desire: Desire) -> None:
    super().__init__()
    self.desire = desire

  def to_dict(self) -> Dict[str, Any]:
    return {
      "desire": self.desire.to_dict()
    }