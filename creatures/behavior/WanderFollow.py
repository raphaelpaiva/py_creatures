from creatures.behavior.MoveTo import MoveTo
from creatures.behavior.Wander import Wander
from creatures.behavior.behavior_abstract import Behavior
from creatures.entity import Entity
from creatures.location import Location
from creatures.world import World

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
