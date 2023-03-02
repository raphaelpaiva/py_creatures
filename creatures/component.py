from creatures.primitives import Vector

class Component(object):
  def __init__(self) -> None:
    self.properties = {}

class MetaDataComponent(Component):
  def __init__(self, name: str = '', type: str = '') -> None:
    super().__init__()
    self.name = name
    self.type = type

class MovementComponent(Component):
  def __init__(self, position: Vector = Vector(0, 0)) -> None:
    self.position:     Vector = position
    self.velocity:     Vector = Vector(0, 0)
    self.acceleration: Vector = Vector(0, 0)