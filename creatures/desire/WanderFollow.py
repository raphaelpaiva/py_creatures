from creatures.desire.MoveTo import MoveTo
from creatures.desire.Wander import Wander
from creatures.desire.desire_abstract import Desire
from creatures.entity import Entity
from creatures.location import Location
from creatures.world import World

class WanderFollow(Desire):
  def __init__(self, entity: Entity, world: World = None) -> None:
    super().__init__(entity)
    self.world = world
    self.desire = Wander(entity, world=self.world)
  
  def run(self):
    self.desire.entity = self.entity
    if isinstance(self.desire, Wander):
      near_entity = self.world.any_near(self.entity)
      if near_entity:
        self.desire = MoveTo(self.entity, Location(lambda: near_entity.movement.position), world=self.world)
    elif isinstance(self.desire, MoveTo):
      sensor_radius = self.entity.properties.get('sensor_radius', 7.0)
      distance = self.entity.distance(self.desire.location.get())

      if distance > sensor_radius:
        self.desire = Wander(self.entity, world=self.world)
    
    self.desire.run()
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.desire})"
