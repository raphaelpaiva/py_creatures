from typing import Any, Dict
from creatures.behavior_abstract import Behavior
from creatures.entity import Entity
from creatures.location import Location, Somewhere
from creatures.primitives import Vector
from creatures.world import World


class MoveTo(Behavior):
  def __init__(self, entity: Entity, location: Location, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity)
    self.location = location
    self.never_satisfied = never_satisfied
    self.world = world
  
  def run(self):
    speed = self.entity.properties.get('speed', 1.0)
    direction = Vector.from_points(self.entity.movement.position, self.location.get()).unit()
    self.entity.movement.velocity = direction.scalar(speed)

  def satisfied(self):
    if self.never_satisfied:
      return False
    else:
      return self.entity.movement.position == self.location.get()
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "location": self.location.to_dict(),
      "never_satisfied": self.never_satisfied
    }
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.location})"

class MoveRelative(MoveTo):
  def __init__(self, entity: Entity, location: Vector, never_satisfied=False, world: World = None) -> None:
    super().__init__(entity, location, never_satisfied, world)
  
  def run(self):
    self.entity.movement.velocity += self.location.get().scalar(self.entity.properties.get('speed', 1.0))
  
  def satisfied(self):
    return not self.never_satisfied

class StayStill(Behavior):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
  
  def satisfied(self):
    return True
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id
    }

class Wander(Behavior):
  def __init__(self, entity: Entity, max_distance: float = 30.0, world: World = None) -> None:
    super().__init__(entity)
    self.max_distance = max_distance
    self.current_movement = None
    self.world = world

  def run(self):
    max_x, max_y = self.world.width - 1, self.world.height - 1 if self.world else (100, 100)

    if not self.current_movement:
      self.current_movement = self.next_movement(max_x, max_y)
    if self.current_movement.satisfied():
      self.current_movement = self.next_movement(max_x, max_y)
    else:
      self.current_movement.run()

  def next_movement(self, max_x: float, max_y: float) -> MoveTo:
    return MoveTo(self.entity, self._next_location(max_x, max_y), world=self.world)
  
  def _next_location(self, max_x: float, max_y: float) -> Location:
    somewhere = Somewhere(max_x, max_y).get()

    direction = Vector.from_points(
      self.entity.movement.position,
      somewhere
    )

    restricted_direction = self.entity.movement.position + direction.unit().scalar(self.max_distance)
      
    return Location(restricted_direction)
  
  def to_dict(self):
    return {
      'type': self.type,
      'current_movement': self.current_movement.to_dict() if self.current_movement else None
    }

class WanderFollow(Behavior):
  def __init__(self, entity: Entity, world: World = None) -> None:
    super().__init__(entity)
    self.world = world
    self.behavior = Wander(entity, world=self.world)
  
  def run(self):
    self.behavior.entity = self.entity
    if isinstance(self.behavior, Wander):
      near_entity = self.world.any_near(self.entity)
      if near_entity:
        self.behavior = MoveTo(self.entity, Location(lambda: near_entity.movement.position), world=self.world)
    elif isinstance(self.behavior, MoveTo):
      sensor_radius = self.entity.properties.get('sensor_radius', 7.0)
      distance = self.entity.distance(self.behavior.location.get())

      if distance > sensor_radius:
        self.behavior = Wander(self.entity, world=self.world)
    
    self.behavior.run()
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.behavior})"


class Grab(Behavior):
  def __init__(self, entity: Entity, resource: Entity, world=None) -> None:
    super().__init__(entity)
    self.resource = resource
    self.world
    self.underlying_behavior = MoveTo(self.entity, Location(resource), world=self.world)
  
  def run(self):
    if self.underlying_behavior.satisfied():
      self.entity.inventory.append(self.resource)
      self.resource.mark_remove = True
      self.entity.behavior = MoveTo(self.entity, Location(Vector(100, 0)), world=self.world)
    else:
      self.underlying_behavior.run()
  
  def satisfied(self):
    return False
  
  @property
  def entity(self) -> Entity:
    return self._entity

  @entity.setter
  def entity(self, entity: Entity) -> Entity:
    super().entity = entity
    self.underlying_behavior.entity = entity
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "resource": self.resource.id
    }
