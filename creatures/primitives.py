from __future__ import annotations
from math import isclose
from typing import Any, Dict
import numpy as np

class Vector(object):
  def __init__(self, x: float = 0, y: float = 0, vec = None) -> None:
    super().__init__()
    self._vec = np.array([x, y]) if vec is None else vec
  
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
    return Vector(vec=self._vec * value)

  def div(self, value: Any[float, int]) -> Vector:
    return self * (1.0 / value)

  def add(self, other: Vector) -> Vector:
    return Vector(vec=self._vec + other._vec)

  def sub(self, other: Vector) -> Vector:
    return Vector(vec=self._vec - other._vec)

  def size(self) -> float:
    return np.sqrt(np.power(self._vec, [2, 2]))
    #return sqrt(self.x * self.x + self.y * self.y)

  def unit(self) -> Vector:
    return Vector(vec=self._vec / self.size())
  
  def scalar(self, mult: float) -> Vector:
    return Vector(vec=self._vec * mult)

  def as_tuple(self):
    return (self.x, self.x)
  
  @property
  def x(self) -> float:
    return self._vec[0]
  
  @property
  def y(self) -> float:
    return self._vec[1]


  def __eq__(self, __o: object) -> bool:
    return isinstance(__o, Vector) and ( isclose(self.x, __o.x, rel_tol=1e-1) and isclose(self.y, __o.y, rel_tol=1e-1))

  def __str__(self) -> str:
    return f"Vec({self.x:.2f}, {self.y:.2f})"
