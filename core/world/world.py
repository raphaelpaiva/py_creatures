from __future__ import annotations

import logging
from time import time

from core.entity import Entity
from core.primitives import Vector

from core.system import System
from copy import deepcopy

from typing import Any, Dict, Iterable, List


class World(object):
  def __init__(self, width: int = 100, height: int = 100, random_seed=None) -> None:
    self.log = logging.getLogger(self.__class__.__name__)
    self.time_resolution = 10.0
    self._height = width
    self._width = height
    self.size = Vector(width, height)
    self._dt = 0.000001
    self.entities_map: Dict[str, Entity] = {}
    self.systems: List[System] = []
    self.random_seed = int(time()) if not random_seed else random_seed
    self._clock = 0.0

  def update(self, external_dt: float = None):
    update_start = time()
    
    for system in self.systems:
      system.update(self.entities())

    for entity in [a for a in self.entities() if a.remove]:
      self.log.info(f"Entity {entity.id} removed.")
      self.remove(entity)
    
    update_end = time()
    self.dt = external_dt if external_dt else (update_end - update_start)
  
  def add(self, entity: Entity) -> None:
    self.entities_map[entity.id] = entity

  def remove(self, entity: Entity) -> None:
    self.entities_map.pop(entity.id)

  def entities(self) -> List[Entity]:
    return list(self.entities_map.values())
  
  def any_near(self, entity: Entity) -> Entity | None:
    for other_entity in self.entities():
      distance = entity.distance(other_entity)
      if 0 < distance <= entity.properties.get('sensor_radius', 7.0):
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

  @property
  def dt(self):
    return self._dt

  @dt.setter
  def dt(self, new_dt):
    self._dt = new_dt * self.time_resolution
    self._clock += self._dt

  @property
  def clock(self):
    return self._clock

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