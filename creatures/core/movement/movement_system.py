from typing import List
from creatures.core.entity import Entity
from creatures.core.system import System
from creatures.core.world import World


class MovementSystem(System):
  """
  A system responsible for updating the movement of entities based on their velocity.

  Attributes:
      world (World): The world instance where the system operates.
      processing_list (List[Entity]): A list of entities to process in the system.

  Methods:
      update(entities): Update the movement of entities based on their velocity.
  """
  def __init__(self, world: World) -> None:
    """
    Initialize a MovementSystem object.

    Args:
        world (World): The world instance where the system operates.
    """
    super().__init__(world)
    self.processing_list: List[Entity] = []
  
  def update(self, entities: List[Entity]):
    """
    Update the movement of entities based on their velocity.

    Args:
        entities (List[Entity]): The list of entities to update.
    """
    for entity in entities:
      entity.movement.position += entity.movement.velocity * self.world.dt
