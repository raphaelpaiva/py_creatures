from typing import Any, Dict

import app.action
from app.desire.MoveTo import MoveTo
from app.action import ActionComponent
from app.desire.desire_abstract import Desire
from core.entity import Entity
from app.location import Location
from core.world import World


class Grab(Desire):
  def __init__(self, entity: Entity, resource: Entity, world=None) -> None:
    super().__init__(entity)
    self.resource = resource
    self.world = world
    self.grab_radius = self.entity.properties.get('grab_radius', 0.0)
    self.action_component: ActionComponent = self.entity.get_component(ActionComponent)
    self.underlying_desire = MoveTo(self.entity, Location(resource), world=self.world)
    self._satisfied = False
  
  def run(self, world: World = None):
    if self.satisfied():
      return

    target_in_grab_range: bool = self.entity.distance(self.resource) <= self.grab_radius
    if target_in_grab_range:
      self.action_component.action = app.action.Grab(self.entity, self.resource)
      self._satisfied = True
    else:
      self.underlying_desire.run()
  
  def satisfied(self):
    return self._satisfied
  
  @property
  def entity(self) -> Entity:
    return self._entity

  @entity.setter
  def entity(self, entity: Entity):
    self._entity = entity
    self.underlying_desire.entity = entity
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "resource": self.resource.id
    }

  def __str__(self):
    return f"grab {self.resource.name}"
