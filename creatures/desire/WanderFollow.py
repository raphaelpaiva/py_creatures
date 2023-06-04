from creatures.action.action import ActionComponent, Grab
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
    self.target = None
  
  def run(self):
    self.desire.entity = self.entity
    if isinstance(self.desire, Wander):
      near_entity = self.world.any_near(self.entity)
      if near_entity:
        self.target = near_entity
        self.desire = MoveTo(self.entity, Location(lambda: near_entity.movement.position), world=self.world)
    elif isinstance(self.desire, MoveTo):
      sensor_radius = self.entity.properties.get('sensor_radius', 7.0)
      distance = self.entity.distance(self.desire.location.get())

      if distance > sensor_radius:
        self.desire = Wander(self.entity, world=self.world)
        self.target = None
      else:
        grab_radius = self.entity.properties.get('grab_radius', 2.0)
        if distance <= grab_radius:
          action_component = self.entity.get_component(ActionComponent.__name__)
          if action_component:
            action_component.action = Grab(self.entity, self.target)
            self.desire = Wander(self.entity, world=self.world)
            self.target = None
            return
      
      if self.target and self.target.mark_remove:
        self.target = None
        self.desire = Wander(self.entity, world=self.world)
    
    self.desire.run()
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.desire})"

