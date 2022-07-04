from __future__ import annotations
from collections import OrderedDict
from copy import deepcopy

from math import sqrt, isclose
import random
import yaml
from typing import Any, ClassVar, Dict, List

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
    return f"Vec({self.x}, {self.y})"

class Location(object):
  def __init__(self, location: Any[Entity, Vector]) -> None:
    super().__init__()
    self.location = location
    self.type = location.__class__.__name__

  def get(self) -> Vector:
    return self.location if self.type == "Vector" else self.location.position
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "location": self.location.to_dict(),
      "type": self.type
    }

class Somewhere(Location):
  def __init__(self, max_x: float = 100, max_y: float = 100) -> None:
    location = Vector(random.random() * max_x, random.random() * max_y)
    super().__init__(location)

class Action(object):
  def __init__(self, entity: Entity) -> None:
    super().__init__()
    self.entity = entity

  def run(self): pass
  def satisfied(self): pass
  def to_dict(self): pass
  
  @property
  def entity(self):
    return self._entity
  
  @entity.setter
  def entity(self, other: Entity):
    self._entity = other

class MoveTo(Action):
  def __init__(self, entity: Entity, location: Location, never_satisfied=False) -> None:
    super().__init__(entity)
    self.location = location
    self.never_satisfied = never_satisfied
  
  def run(self):
    speed = self.entity.properties.get('speed', 1.0)
    direction = Vector.from_points(self.entity.position, self.location.get()).unit()
    velocity = direction.scalar(speed)
    self.entity.position += velocity

  def satisfied(self):
    if self.never_satisfied:
      return False
    else:
      return self.entity.position == self.location.get()
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "entity": self.entity.id,
      "location": self.location.to_dict(),
      "never_satisfied": self.never_satisfied
    }

class StayStill(Action):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
  
  def satisfied(self):
    return True
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "entity": self.entity.id
    }

class MoveAround(Action):
  def __init__(self, entity: Entity, max_distance: float = 10.0) -> None:
    super().__init__(entity)
    self.max_distance = max_distance
    self.current_movement = MoveTo(self.entity, self._next_location())

  def run(self):
    if self.current_movement.satisfied():
      self.current_movement = MoveTo(self.entity, self._next_location())
    else:
      self.current_movement.run()
  
  def _next_location(self) -> Location:
    somewhere = Somewhere().get()

    direction = Vector.from_points(
      self.entity.position,
      somewhere
    )

    restricted_direction = self.entity.position + direction.unit().scalar(self.max_distance)
      
    return Location(restricted_direction)

class Grab(Action):
  def __init__(self, entity: Entity, resource: Resource) -> None:
    super().__init__(entity)
    self.resource = resource
    self.underlying_action = MoveTo(self.entity, Location(resource))
  
  def run(self):
    if self.underlying_action.satisfied():
      self.entity.inventory.append(self.resource)
      self.resource.mark_remove = True
      self.entity.action = MoveTo(self.entity, Location(Vector(100, 0)))
    else:
      self.underlying_action.run()
  
  def satisfied(self):
    return False
  
  @property
  def attach(self, entity: Entity):
    super().entity = entity
    self.underlying_action.entiry = entity
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "entity": self.entity.id,
      "resource": self.resource.id
    }

class Entity(object):
  def __init__(self, id: str, position: Vector) -> None:
    super().__init__()
    self.id = id
    self.position = position if position else Somewhere().get()
    self.size = 10
    self.action: Action = MoveAround(self)
    self.world: World = None
    self.inventory = []
    self.mark_remove = False
    self.properties: Dict[str, str] = {}

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
      "action": self.action.to_dict() if self.action else None,
      "inventory": [r.to_dict() for r in self.inventory],
      "mark_remove": self.mark_remove,
    }

class Resource(Entity):
  def __init__(self, id: str, position: Vector) -> None:
    super().__init__(id, position)
    self.action = StayStill(self)
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.__class__.__name__,
      "id": self.id,
      "position": self.position.to_dict(),
      "size": self.size,
      "action": self.action.to_dict(),
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
      entity.action.run()
      if entity.action.satisfied():
        entity.action = StayStill(entity)

    for entity in [a for a in self.entities() if a.mark_remove]:
      self.remove(entity)
  
  def add(self, entity: Entity):
    entity.world = self
    self.entities_map[entity.id] = entity

  def remove(self, entity: Entity):
    self.entities_map.pop(entity.id)

  def entities(self):
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
      "type": self.__class__.__name__,
      "number": self.number,
      "world": self.world.to_dict()
    }

def frame_generator(keyframe: Frame):
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

  maria.action = Grab(maria, food_1)
  ze.action    = Grab(ze, food_1)

  w = World()
  w.add(ze)
  w.add(maria)
  w.add(food_1)
  w.add(food_2)
  return w