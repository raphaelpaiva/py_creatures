from typing import Any, Callable, Dict, Union
from core.entity import Entity
from core.primitives import Vector
from core.random_generator import generator as random


class Location(object):
  def __init__(self, location: Union[Callable, Vector, Entity], identifier: str = None) -> None:
    super().__init__()
    self.target = location
    self.type = location.__class__.__name__
    self.identifier = self.target if isinstance(self.target, Entity) and identifier is None else ''

  def get(self) -> Vector:
    if isinstance(self.target, Vector):
      return self.target
    if isinstance(self.target, Callable):
      return self.target()
    if isinstance(self.target, Entity):
      return self.target.movement.position
    
    return None
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "location": self.target.to_dict() if self.type == "Vector" else self.target
    }
  
  def __str__(self) -> str:
    location_str = self.identifier if callable(self.target) else str(self.target)
    return str(location_str)


class Somewhere(Location):
  def __init__(self, max_x: float = 100, max_y: float = 100) -> None:
    location = Vector(random.random() * max_x, random.random() * max_y)
    super().__init__(location)