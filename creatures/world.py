from __future__ import annotations
from time import time

from creatures.entity import Entity
from creatures.primitives import Vector

from .system import System
from copy import deepcopy

from typing import Any, Dict, Iterable, List

class World(object):
  def __init__(self, width: int = 100, height: int = 100) -> None:
    self.TIME_RESOLUTION = 1.0
    self._height = width
    self._width  = height
    self.dt      = 0.000001
    self.entities_map: Dict[str, Entity] = {}
    self.systems: List[System] = []

  def update(self):
    update_start = time()
    
    for system in self.systems:
      system.accept(self.entities())
      system.update()

    for entity in [a for a in self.entities() if a.mark_remove]:
      self.remove(entity)
    
    update_end = time()
    self.dt = (update_end - update_start) * self.TIME_RESOLUTION
  
  def add(self, entity: Entity) -> None:
    self.entities_map[entity.id] = entity

  def remove(self, entity: Entity) -> None:
    self.entities_map.pop(entity.id)

  def entities(self) -> List[Entity]:
    return list(self.entities_map.values())
  
  def any_near(self, entity: Entity) -> Entity | None:
    for other_entity in self.entities():
      distance = entity.distance(other_entity)
      if distance > 0 and distance <= entity.properties.get('sensor_radius', 7.0):
        return other_entity
    return None

  def add_system(self, system: System):
    self.systems.append(system)

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
  food_1 = Entity('food_1', Vector(75, 90))
  food_2 = Entity('food_2', Vector(10, 10))

  w = World()
  w.add(ze)
  w.add(maria)
  w.add(food_1)
  w.add(food_2)
  return w