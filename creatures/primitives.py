from __future__ import annotations
from math import isclose, sqrt
from typing import Any, Dict

class Vector(object):
  def __init__(self, x: float, y: float) -> None:
    super().__init__()
    self._x: float = x
    self._y: float = y
  
  @classmethod
  def from_points(cls, origin: Vector, dest: Vector) -> Vector:
    x = dest.x - origin.x
    y = dest.y - origin.y

    return Vector(x, y)
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "x": self.x,
      "y": self.y
    }

  def __add__(self, other: Vector) -> Vector:
    return self.add(other)
  
  def __sub__(self, other: Vector) -> Vector:
    return self.sub(other)

  def __truediv__(self, other: float) -> Vector:
    return self.div(other)

  def __mul__(self, other: float) -> Vector:
    return self.mul(other)

  def mul(self, value: Any[float, int]) -> Vector:
    return Vector(self.x * value, self.y * value)

  def div(self, value: Any[float, int]) -> Vector:
    return self * (1.0 / value)

  def add(self, vec: Vector) -> Vector:
    return Vector(self.x + vec.x, self.y + vec.y)

  def sub(self, vec: Vector) -> Vector:
    return Vector(self.x - vec.x, self.y - vec.y)

  def size(self) -> float:
    return sqrt(self.x * self.x + self.y * self.y)

  def unit(self) -> Vector:
    return self / self.size()
  
  def scalar(self, mult: float) -> Vector:
    return Vector(self.x * mult, self.y * mult)

  @property
  def x(self) -> float:
    return self._x
  
  @property
  def y(self) -> float:
    return self._y

  def __eq__(self, __o: object) -> bool:
    return isinstance(__o, Vector) and ( isclose(self.x, __o.x, rel_tol=1e-1) and isclose(self.y, __o.y, rel_tol=1e-1))

  def __str__(self) -> str:
    return f"Vec({self.x:.2f}, {self.y:.2f})"
