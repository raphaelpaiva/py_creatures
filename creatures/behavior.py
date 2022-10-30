from typing import Any, Dict
from .world import Behavior, Entity, Location, Resource, Somewhere, Vector

class MoveTo(Behavior):
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
      "type": self.type,
      "entity": self.entity.id,
      "location": self.location.to_dict(),
      "never_satisfied": self.never_satisfied
    }

class MoveRelative(MoveTo):
  def __init__(self, entity: Entity, location: Vector, never_satisfied=False) -> None:
    super().__init__(entity, location, never_satisfied)
  
  def run(self):
    self.entity.position += self.location
  
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
  def __init__(self, entity: Entity, max_distance: float = 10.0) -> None:
    super().__init__(entity)
    self.max_distance = max_distance
    self.current_movement = None

  def run(self):
    if not self.current_movement:
      self.current_movement = self.next_movement()
    if self.current_movement.satisfied():
      self.current_movement = self.next_movement()
    else:
      self.current_movement.run()

  def next_movement(self) -> MoveTo:
    return MoveTo(self.entity, self._next_location())
  
  def _next_location(self) -> Location:
    somewhere = Somewhere().get()

    direction = Vector.from_points(
      self.entity.position,
      somewhere
    )

    restricted_direction = self.entity.position + direction.unit().scalar(self.max_distance)
      
    return Location(restricted_direction)
  
  def to_dict(self):
    return {
      'type': self.type,
      'current_movement': self.current_movement.to_dict() if self.current_movement else None
    }


class Grab(Behavior):
  def __init__(self, entity: Entity, resource: Resource) -> None:
    super().__init__(entity)
    self.resource = resource
    self.underlying_behavior = MoveTo(self.entity, Location(resource))
  
  def run(self):
    if self.underlying_behavior.satisfied():
      self.entity.inventory.append(self.resource)
      self.resource.mark_remove = True
      self.entity.behavior = MoveTo(self.entity, Location(Vector(100, 0)))
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
