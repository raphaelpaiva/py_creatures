from typing import Any, Dict
from core.primitives import Vector

class Component(object):
  def __init__(self) -> None:
    self.properties = {}
  def to_dict(self) -> Dict[str, Any]: return {}

class MetaDataComponent(Component):
  def __init__(self, name: str = '', type: str = '') -> None:
    super().__init__()
    self.name = name
    self.type = type
  def to_dict(self) -> Dict[str, Any]:
    return {
      "name": self.name,
      "type": self.type
    }

class MovementComponent(Component):
  def __init__(self, position: Vector = Vector(0, 0)) -> None:
    self.position:     Vector = position
    self.velocity:     Vector = Vector(0, 0)
    self.acceleration: Vector = Vector(0, 0)
  def to_dict(self) -> Dict[str, Any]:
    return {
      "position":     self.position.to_dict(),
      "velocity":     self.velocity.to_dict(),
      "acceleration": self.acceleration.to_dict(),
    }

class EnergyComponent(Component):
  def __init__(self, max_energy: float = 100.0, rate: float = 0.01) -> None:
    super().__init__()
    self.max_energy = max_energy
    self._current    = max_energy
    self.rate       = rate
  
  @property
  def current(self) -> float:
    return self._current
  
  @current.setter
  def current(self, value: float):
    self._current = min(self.max_energy, value)

  def __str__(self) -> str:
    return f"{int(self.current)}/{int(self.max_energy)}"
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "max_energy": self.max_energy,
      "current": self.current,
      "rate": self.rate,
    }