from abc import ABC, abstractmethod
from core.entity import Entity


class DietReasoner(ABC):
  def __init__(self): pass
  @abstractmethod
  def is_edible(self, entity: Entity): pass
