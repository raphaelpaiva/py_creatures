from typing import Any, Dict
from creatures.desire.MoveTo import MoveTo
from creatures.desire.desire_abstract import Desire
from creatures.entity import Entity
from creatures.location import Location
from creatures.primitives import Vector


class Grab(Desire):
  def __init__(self, entity: Entity, resource: Entity, world=None) -> None:
    super().__init__(entity)
    self.resource = resource
    self.world
    self.underlying_desire = MoveTo(self.entity, Location(resource), world=self.world)
  
  def run(self):
    if self.underlying_desire.satisfied():
      self.entity.inventory.append(self.resource)
      self.resource.mark_remove = True
      self.entity.desire = MoveTo(self.entity, Location(Vector(100, 0)), world=self.world)
    else:
      self.underlying_desire.run()
  
  def satisfied(self):
    return False
  
  @property
  def entity(self) -> Entity:
    return self._entity

  @entity.setter
  def entity(self, entity: Entity) -> Entity:
    super().entity = entity
    self.underlying_desire.entity = entity
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "type": self.type,
      "entity": self.entity.id,
      "resource": self.resource.id
    }
