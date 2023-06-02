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

class EnergyComponent(Component):
  def __init__(self, max_energy: float = 100.0, rate: float = 0.01) -> None:
    super().__init__()
    self.max_energy = max_energy
    self.current    = max_energy
    self.rate       = rate
  
  def __str__(self) -> str:
    return f"{int(self.current)}/{int(self.max_energy)}"