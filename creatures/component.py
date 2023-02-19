from creatures.primitives import Vector

class Component(object):
  def __init__(self) -> None:
    self.properties = {}

class MetaDataComponent(Component):
  def __init__(self) -> None:
    super().__init__()
    self.name = ''

class MovementComponent(Component):
  def __init__(self) -> None:
    self.target:       Vector = None
    self.position:     Vector = Vector(0, 0)
    self.velocity:     Vector = Vector(0, 0)
    self.acceleration: Vector = Vector(1, 1)