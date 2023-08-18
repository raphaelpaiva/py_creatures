from typing import List
from abc import ABC, abstractmethod
from creatures.core.entity import Entity


class System(ABC):
  """
  Represents a base class for systems in the simulation.

  Attributes:
      world: The world instance where the system operates.

  Methods:
      update(entities): Update the system based on a list of entities.
  """
  def __init__(self, world) -> None:
    """
    Initialize a System object.

    Args:
        world: The world instance where the system operates.
    """
    self.world = world

  @abstractmethod
  def update(self, entities: List[Entity]):
    """
    Update the system based on a list of entities.

    This method should be overridden by subclasses to implement specific system behavior.

    Args:
        entities (List[Entity]): The list of entities to update.
    """
    pass
