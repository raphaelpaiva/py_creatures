from __future__ import annotations

import logging
from time import time

from creatures.core.entity import Entity
from creatures.core.primitives import Vector

from creatures.core.system import System

from typing import Any, Dict, List

from creatures.core.util import Stats

DEFAULT_TIME_RESOLUTION = .001


class World(object):
  """
  Represents the world containing entities and systems for simulation.

  Attributes:
    log: The logger instance for the world.
    time_resolution (float): The time resolution for simulations.
    _height (int): The height of the world.
    _width (int): The width of the world.
    size (Vector): The size of the world as a vector.
    _dt (float): The time step for simulations.
    entities_map (Dict[str, Entity]): A dictionary of entities in the world.
    systems (List[System]): A list of systems operating in the world.
    random_seed: The random seed for the world.
    _clock (float): The simulation clock.
    stats (WorldStats): The statistics for the world.

  Methods:
    update(external_dt): Update the world simulation.
    add(entity): Add an entity to the world.
    remove(entity): Remove an entity from the world.
    entities(): Get a list of entities in the world.
    any_near(entity): Check if any entity is near a given entity.
    add_system(system): Add a system to the world.
  """
  def __init__(self,
              width: int = 100,
              height: int = 100,
              random_seed=None,
              time_resolution: float = DEFAULT_TIME_RESOLUTION) -> None:
    """
    Initialize a World object.

    Args:
      width (int): The width of the world.
      height (int): The height of the world.
      random_seed: The random seed for the world.
    """
    self.log = logging.getLogger(self.__class__.__name__)
    self.time_resolution = time_resolution
    self._height = width
    self._width = height
    self.size = Vector(width, height)
    self._dt = 0.000001
    self.entities_map: Dict[str, Entity] = {}
    self.systems: List[System] = []
    self.random_seed = int(time()) if not random_seed else random_seed
    self._clock = 0.0
    self.stats = WorldStats()

  def update(self, external_dt: float = None):
    """
    Update the world simulation.

    Updates the world systems by a given delta time. If no delta time is specified, the internal dt will be used.
    The internal dt is the time the last `update()` call took, in milliseconds.

    All times are measured in milliseconds.

    Args:
      external_dt (float): External time step for simulations, in milliseconds. If not specified, the internal dt will be used.
    """
    update_start = time() * 1000

    self.stats.population = len(self.entities_map.keys())
    for system in self.systems:
      system.update(self.entities())

    for entity in [a for a in self.entities() if a.remove]:
      self.log.info(f"Entity {entity.id} removed.")
      self.remove(entity)
      self.stats.removed_count += 1
    
    update_end = time() * 1000
    internal_dt = (update_end - update_start)
    self.dt = external_dt if external_dt else internal_dt
    if external_dt:
      self.dt = external_dt
      self.stats.external_dt = external_dt
    else:
      self.stats.internal_dt = internal_dt
      self.dt = internal_dt
    self.stats.simulation_clock = self.clock
    self.stats.time_resolution = self.time_resolution
  
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
    """
    Get a string representation of the world.

    Returns:
      str: A string representation of the world.
    """
    return f"{self.__class__.__name__}({self.height}, {self.width}, {len(self.entities())})"
  
  def __repr__(self) -> str:
    """
    Get a string representation of the world for debugging.

    Returns:
      str: A string representation of the world.
    """
    return f"{self.__class__.__name__}({self.width, self.height, self.random_seed})"
  
  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the world to a dictionary.

    Returns:
      dict: A dictionary containing information about the world.
    """
    return {
      "type": self.__class__.__name__,
      "width": self.width,
      "height": self.height,
      "entities": [a.to_dict() for a in self.entities()],
    }


class Frame(object):
  """
  Represents a frame in the simulation.

  Attributes:
    _number (int): A static variable to keep track of the frame number.
    number (int): The frame number.
    world (World): The world associated with the frame.

  Methods:
    to_dict(): Convert the frame to a dictionary.
  """
  _number = 0
  
  def __init__(self, world: World) -> None:
    """
    Initialize a Frame object.

    Args:
      world (World): The world associated with the frame.
    """
    super().__init__()
    self.number = Frame._number
    self.world = world
    Frame._number += 1
  
  def __str__(self) -> str:
    """
    Get a string representation of the frame.

    Returns:
      str: A string representation of the frame.
    """
    return f"Frame(#{self.number}, world: {self.world})"

  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the frame to a dictionary.

    Returns:
      dict: A dictionary containing information about the frame.
    """
    return {
      "frame": {
        "type": self.__class__.__name__,
        "number": self.number,
        "world": self.world.to_dict()
      }
    }


class WorldStats(Stats):
  """
  Represents statistics for the world simulation.

  Attributes:
    population (int): The population of entities in the world.
    removed_count (int): The count of removed entities.
    _internal_dt (float): Internal time step for simulations.
    _external_dt (float): External time step for simulations.
    simulation_clock (float): The simulation clock time.
    frame_count (int): The count of frames.
    frame_time_acc (float): Accumulated time for frames.

  Methods:
    get_dict(): Get a dictionary representation of the statistics.
  """
  def __init__(self):
    self.population: int = 0
    self.removed_count: int = 0
    self._internal_dt: float = 0.0
    self._external_dt: float = 0.0
    self.simulation_clock: float = 0.0

    self.frame_count: int = 0
    self.frame_time_acc: float = 0
    self.time_resolution: float = 0.0

  def get_dict(self) -> Dict[str, Any]:
    """
    Get a dictionary representation of the statistics.

    Returns:
      dict: A dictionary containing the statistics data.
    """
    return {
      'population': str(self.population),
      'removed_count': str(self.removed_count),
      'avg_frame_rate': f"{self.avg_frame_rate:.1f}Hz",
      'avg_frame_time': f"{self.avg_frame_time:.2f}ms",
      'simulation_clock': f"{self.simulation_clock:.2f}ms",
      'internal_dt': f"{self.internal_dt:.2f}ms",
      'external_dt': f"{self.external_dt:.2f}ms",
      'frame_count': f"{self.frame_count}",
      'time_resolution': f"{self.time_resolution}",
    }

  @property
  def internal_dt(self):
    return self._internal_dt

  @internal_dt.setter
  def internal_dt(self, new_dt):
    self._internal_dt = new_dt
    self.frame_time_acc += self._internal_dt
    self.frame_count += 1

  @property
  def external_dt(self):
    return self._external_dt

  @external_dt.setter
  def external_dt(self, new_dt):
    self._external_dt = new_dt if new_dt else 0
    self.frame_time_acc += self._external_dt
    self.frame_count += 1

  @property
  def avg_frame_time(self) -> float:
    if self.frame_count == 0:
      return 0.0
    else:
      return self.frame_time_acc / self.frame_count

  @property
  def avg_frame_rate(self) -> float:
    return 1000.0 / (self.avg_frame_time + 0.0000001)
