from __future__ import annotations
from abc import abstractmethod
from copy import deepcopy

from math import sqrt, isclose
import random
from typing import Any, Dict, Iterable, List, Union

class Vector(object):
  def __init__(self, x: float, y: float) -> None:
    super().__init__()
    self._x: float = x
    self._y: float = y
  
  @classmethod
  def from_points(cls, origin: Vector, dest: Vector) -> Vector:
    x = dest.x - origin.x
    y = dest.y - origin.y

    return Vector(x, y)
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "x": self.x,
      "y": self.y
    }

  def __add__(self, other: Vector) -> Vector:
    return self.add(other)
  
  def __sub__(self, other: Vector) -> Vector:
    return self.sub(other)

  def __truediv__(self, other: float) -> Vector:
    return self.div(other)

  def __mul__(self, other: float) -> Vector:
    return self.mul(other)

  def mul(self, value: Any[float, int]) -> Vector:
    return Vector(self.x * value, self.y * value)

  def div(self, value: Any[float, int]) -> Vector:
    return self * (1.0 / value)

  def add(self, vec: Vector) -> Vector:
    return Vector(self.x + vec.x, self.y + vec.y)

  def sub(self, vec: Vector) -> Vector:
    return Vector(self.x - vec.x, self.y - vec.y)

  def size(self) -> float:
    return sqrt(self.x * self.x + self.y * self.y)

  def unit(self) -> Vector:
    return self / self.size()
  
  def scalar(self, mult: float) -> Vector:
    return Vector(self.x * mult, self.y * mult)

  @property
  def x(self):
    return self._x
  
  @property
  def y(self):
    return self._y

  def __eq__(self, __o: object) -> bool:
    return isinstance(__o, Vector) and ( isclose(self.x, __o.x, rel_tol=1e-1) and isclose(self.y, __o.y, rel_tol=1e-1))

  def __str__(self) -> str:
    return f"Vec({self.x:.2f}, {self.y:.2f})"

class Behavior(object):
  def __init__(self, entity: Entity=None) -> None:
    super().__init__()
    self.entity = entity

  @property
  def type(self) -> str:
    return self.__class__.__name__

  @abstractmethod
  def run(self) -> None: pass
  
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

class Location(object):
  def __init__(self, location: Union[Entity, Vector]) -> None:
    super().__init__()
    self._location = location
    self.type = location.__class__.__name__

  def get(self) -> Vector:
    return self._location if self.type == "Vector" else self._location.position
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "location": self._location.to_dict() if self.type == "Vector" else self._location.id
    }

class Somewhere(Location):
  def __init__(self, max_x: float = 100, max_y: float = 100) -> None:
    location = Vector(random.random() * max_x, random.random() * max_y)
    super().__init__(location)

class Entity(object):
  def __init__(self, id: str, position: Vector) -> None:
    super().__init__()
    self.id: str = id
    self.position: Vector = position if position else Somewhere().get()
    self.size: float = 10
    self._behavior: Behavior = None
    self.mark_remove: bool = False
    self.properties: Dict[str, str] = {}
  
  def behavior(self) -> Behavior:
    self.behavior.update()

  @property
  def behavior(self) -> Behavior:
    return self._behavior
  
  @behavior.setter
  def behavior(self, behavior: Behavior):
    self._behavior = behavior
    if self.behavior:
      self.behavior.entity = self

  def __str__(self) -> str:
    return f"{self.__class__.__name__}(id={self.id}, position={self.position})"

  def __repr__(self) -> str:
    return f"{self.__class__.__name__}({self.id}, {self.position})"
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "id": self.id,
      "position": self.position.to_dict(),
      "size": self.size,
      "behavior": self.behavior.to_dict() if self.behavior else None,
      "mark_remove": self.mark_remove,
      "properties": self.properties
    }

class Resource(Entity):
  def __init__(self, id: str, position: Vector) -> None:
    super().__init__(id, position)
    self.behavior = None
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "id": self.id,
      "position": self.position.to_dict(),
      "size": self.size,
      "behavior": self.behavior.to_dict(),
      "inventory": [r.to_dict() for r in self.inventory],
      "mark_remove": self.mark_remove,
    }

class World(object):
  def __init__(self, width: int = 100, height: int = 100) -> None:
    self._height = width
    self._width  = height
    self.entities_map: Dict[str, Entity] = {}

  def update(self):
    for entity in self.entities():
      entity.behavior.run()

    for entity in [a for a in self.entities() if a.mark_remove]:
      self.remove(entity)
  
  def add(self, entity: Entity) -> None:
    self.entities_map[entity.id] = entity

  def remove(self, entity: Entity) -> None:
    self.entities_map.pop(entity.id)

  def entities(self) -> List[Entity]:
    return list(self.entities_map.values())

  @property
  def width(self):
    return self._width
  
  @property
  def height(self):
    return self._height

  def __str__(self) -> str:
    return f"World({self.height}, {self.width}, {len(self.entities())})"
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}()"
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "width": self.width,
      "height": self.height,
      "entities": [a.to_dict() for a in self.entities()],
    }

class Frame(object):
  _number = 0
  
  def __init__(self, world: World) -> None:
    super().__init__()
    self.number = Frame._number
    self.world = world
    Frame._number += 1
  
  def __str__(self) -> str:
    return f"Frame(#{self.number}, world: {self.world})"

  def to_dict(self) -> Dict[str, Any]:
    return {
      "frame": {
        "type": self.__class__.__name__,
        "number": self.number,
        "world": self.world.to_dict()
      }
    }

def frame_generator(keyframe: Frame) -> Iterable[Frame]:
  next_frame = keyframe
  while True:
    yield next_frame
    next_frame.world.update()
    next_frame = Frame(deepcopy(next_frame.world))

def get_example_world() -> World:
  ze     = Entity('Zé', Vector(90, 10))
  maria  = Entity('Maria', Vector(40, 50))
  food_1 = Resource('food_1', Vector(75, 90))
  food_2 = Resource('food_2', Vector(10, 10))

  w = World()
  w.add(ze)
  w.add(maria)
  w.add(food_1)
  w.add(food_2)
  return w