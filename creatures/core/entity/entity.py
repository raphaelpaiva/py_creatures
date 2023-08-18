from __future__ import annotations
from math import sqrt
from typing import Any, Dict
from creatures.core.primitives import Vector
from creatures.core.component import Component, MetaDataComponent, MovementComponent

_ENTITY_IDS: int = -1
DEFAULT_MOVEMENT_COMPONENT = [MovementComponent()]
DEFAULT_METADATA_COMPONENT = [MetaDataComponent()]

def _next_id() -> int:
  global _ENTITY_IDS
  _ENTITY_IDS += 1
  return _ENTITY_IDS


class Entity(object):
  """
  Represents an entity in the system.

  Attributes:
    id (str): The unique identifier of the entity.
    remove (bool): Flag indicating if the entity should be removed.
    properties (dict): Dictionary holding additional properties of the entity.
    type (str): Type of the entity.
    _components (dict): Dictionary holding the components attached to the entity.

  Methods:
    add_component(component): Add a component to the entity.
    get_component(component_id): Get a specific component of the entity.
    mark_remove(): Mark the entity for removal.
    metadata(): Get the metadata component of the entity.
    movement(): Get the movement component of the entity.
    is_resource(): Check if the entity is a resource.
    name(): Get the name of the entity.
    size(): Get the size of the entity.
    distance(other): Calculate the distance to another entity or vector.
    __str__(): Get a string representation of the entity.
    __repr__(): Get a detailed string representation of the entity.
    to_dict(): Convert the entity and its components to a dictionary.
  """
  def __init__(self, id: str, entity_type: str = None) -> None:
    """
    Initialize an Entity object.

    Args:
      id (str): The unique identifier of the entity.
      entity_type (str, optional): Type of the entity. Defaults to a generated id.
    """
    super().__init__()
    self.id: str = id if id is not None else str(_next_id())
    self.remove: bool = False
    self.properties: Dict[str, Any] = {}
    self.type = entity_type if entity_type else self.__class__.__name__
    self._components: Dict[str, Component] = {}

  def add_component(self, component: Component):
    """
    Add a component to the entity.

    Args:
      component (Component): The component to be added.
    """
    component_type_name = component.__class__.__qualname__
    self._components[component_type_name] = component
  
  def get_component(self, component_id: str | type) -> Component | None:
    """
    Get a specific component of the entity.

    Args:
      component_id (str or type): Identifier or type of the component. The identifier is the type name.s

    Returns:
      Component or None: The requested component or None if not found.
    """
    name = component_id
    if isinstance(component_id, type):
      name = component_id.__name__
    
    return self._components.get(name, None)
  
  def mark_remove(self):
    """
    Mark the entity for removal.
    """
    self.remove = True

  @property
  def metadata(self) -> MetaDataComponent:
    """
    Get the metadata component of the entity.

    Returns:
      MetaDataComponent: The metadata component of the entity.
    """
    return self._components.get(MetaDataComponent.__name__, DEFAULT_METADATA_COMPONENT)
  
  @property
  def movement(self) -> MovementComponent:
    """
    Get the movement component of the entity.

    Returns:
      MovementComponent: The movement component of the entity.
    """
    return self._components.get(MovementComponent.__name__, DEFAULT_MOVEMENT_COMPONENT)
  
  @property
  def is_resource(self) -> bool:
    """
    Check if the entity is a resource.

    Returns:
      bool: True if the entity is a resource, False otherwise.
    """
    return self.metadata.type.lower() == 'resource'

  @property
  def name(self) -> str:
    """
    Get the name of the entity.

    Returns:
      str: The name of the entity.
    """
    return self.properties.get('name', self.id)
  
  @property
  def size(self) -> float:
    """
    Get the size of the entity.

    Returns:
      float: The size of the entity.
    """
    return self.properties.get('size', 2.0)
  
  @size.setter
  def size(self, other: float):
    """
    Set the size of the entity.

    Args:
      other (float): The new size for the entity.
    """
    self.properties['size'] = other

  def distance(self, other: Entity | Vector) -> float:
    """
    Calculate the distance to another entity or vector.

    Args:
      other (Entity or Vector): The other entity or vector.

    Returns:
      float: The distance to the other entity or vector.
    """
    v1 = self.movement.position
    v2 = other.movement.position if isinstance(other, Entity) else other

    x_diff = v1.x - v2.x
    y_diff = v1.y - v2.y
    return sqrt( x_diff * x_diff + y_diff * y_diff)

  def __str__(self) -> str:
    return f"{self.__class__.__name__}({self.name})"

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.id}, {self.movement.position})"
  
  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the entity and its components to a dictionary.

    Returns:
      dict: A dictionary representation of the entity.
    """
    components_dict = {k: v.to_dict() for k,v in self._components.items()}
    return {
      "type": self.type,
      "id": self.id,
      "position": components_dict,
      "size": self.size,
      "mark_remove": self.remove,
      "properties": self.properties
    }
