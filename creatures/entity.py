from __future__ import annotations
from math import sqrt
from typing import Any, Dict, List
from creatures.location import Location, Somewhere
from creatures.primitives import Vector
from .component import Component, MetaDataComponent, MovementComponent

_ENTITY_IDS: int = -1
DEFAULT_MOVEMENT_COMPONENT = [MovementComponent()]
DEFAULT_METADATA_COMPONENT = [MetaDataComponent()]

def _next_id() -> int:
  _ENTITY_IDS += 1
  return _ENTITY_IDS
 
class Entity(object):
  def __init__(self, id: str) -> None:
    super().__init__()
    self.id: str = id if id is not None else str(_next_id())
    self.mark_remove: bool = False
    self.properties: Dict[str, Any] = {}
    self.type = self.__class__.__name__
    self.components: Dict[str, List[Component]] = {}

  def add_component(self, component: Component):
    component_type_name = component.__class__.__name__
    if component_type_name in self.components:
      self.components[component_type_name].append(component)
    else:
      self.components[component_type_name] = [component]
  
  @property
  def metadata(self) -> MetaDataComponent:
    return self.components.get(MetaDataComponent.__name__, DEFAULT_METADATA_COMPONENT)[0]
  
  @property
  def movement(self) -> MovementComponent:
    return self.components.get(MovementComponent.__name__, DEFAULT_MOVEMENT_COMPONENT)[0]
  
  @property
  def is_resource(self) -> bool:
    return self.metadata.type.lower() == 'resource'

  @property
  def name(self) -> str:
    return self.properties.get('name', self.id)
  
  @property
  def size(self) -> float:
    return self.properties.get('size', 2.0)
  
  @size.setter
  def size(self, other: float):
    self.properties['size'] = other

  def distance(self, other: Entity | Vector) -> float:
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
    return {
      "type": self.type,
      "id": self.id,
      "position": self.position.to_dict(),
      "size": self.size,
      "mark_remove": self.mark_remove,
      "properties": self.properties
    }
