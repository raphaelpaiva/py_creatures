from core.action.action import ActionComponent, Grab
from core.desire.MoveTo import MoveTo
from core.desire.Wander import Wander
from core.desire.desire_abstract import Desire
from core.entity import Entity
from core.location import Location
from core.sensor.sensor import RadialSensor
from core.sensor.sensor_component import SensorComponent
from core.world import World

class WanderFollow(Desire):
  def __init__(self, entity: Entity, world: World = None) -> None:
    super().__init__(entity)
    self.world = world
    self.desire = Wander(entity, world=self.world)
    self.target = None

  def run(self):
    self.desire.entity = self.entity
    
    # If we're wandering, check for detected entities. If there's any, follow it.
    if isinstance(self.desire, Wander):
      target = self.choose_target()
      if target:
        self.follow(target)
    # If we're Following, check if our target is still in range
    elif isinstance(self.desire, MoveTo):
      sensor_radius = self.get_sensor_radius()
      distance = self.entity.distance(self.desire.location.get())

      # if we can't detect the target anymore, get back to wander
      if distance > sensor_radius:
        self.wander()
      # if we still can, try to grab it.
      else:
        # TODO: Make grab range a sensor and move this out of here. This is Wander of Follow. Grabbing should be a different decision
        grab_radius = self.entity.properties.get('grab_radius', 2.0)
        if distance <= grab_radius:
          action_component = self.entity.get_component(ActionComponent.__name__)
          if action_component:
            # Grab and wander
            action_component.action = Grab(self.entity, self.target)
            self.wander()
            return
      
      # if target is marked for removal from the scene
      if self.target and self.target.mark_remove:
        self.wander()
    
    self.desire.run()

  def get_sensor_radius(self) -> float:
      sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
      return sensor_component.max_radius() if sensor_component else 0.0

  def choose_target(self) -> Entity | None:
    sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
    if sensor_component and sensor_component.detected:
      return list(sensor_component.detected)[0]
    else:
      return None

  def wander(self):
    self.target = None
    self.desire = Wander(self.entity, world=self.world)

  def follow(self, target: Entity):
      self.target = target
      self.desire = MoveTo(self.entity, Location(lambda: target.movement.position), world=self.world)
  
  def to_dict(self):
    return {
      'type': self.__class__.__name__,
      'desire': self.desire.to_dict(),
      'target': self.target.id if self.target else None
    }
  
  def __str__(self) -> str:
    return f"{super().__str__()}({self.desire})"

