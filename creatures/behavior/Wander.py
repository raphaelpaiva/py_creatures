from creatures.behavior.MoveTo import MoveTo
from creatures.behavior.behavior_abstract import Behavior
from creatures.entity import Entity
from creatures.location import Location, Somewhere
from creatures.primitives import Vector
from creatures.world import World


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
