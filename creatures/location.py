import random
from typing import Any, Callable, Dict, Union
from creatures.primitives import Vector

class Location(object):
  def __init__(self, location: Union[Callable, Vector]) -> None:
    super().__init__()
    self._location = location
    self.type = location.__class__.__name__

  def get(self) -> Vector:
    return self._location if self.type == "Vector" else self._location()
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "location": self._location.to_dict() if self.type == "Vector" else self._location
    }
  
  def __str__(self) -> str:
    return str(self._location)

class Somewhere(Location):
  def __init__(self, max_x: float = 100, max_y: float = 100) -> None:
    location = Vector(random.random() * max_x, random.random() * max_y)
    super().__init__(location)