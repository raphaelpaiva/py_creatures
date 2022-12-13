from .world import Entity, Vector

class Component(object):
  def __init__(self, entity: Entity) -> None:
    self.entity: Entity = entity
    self.properties = {}

class MovementComponent(Component):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
    self.target:       Vector = None
    self.position:     Vector = None
    self.velocity:     Vector = None
    self.acceleration: Vector = None