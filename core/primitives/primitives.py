from __future__ import annotations
from math import isclose, sqrt
from typing import Any, Dict, Tuple


class Vector(object):
  """
  Represents a 2D vector with various mathematical operations.
  This class is immutable.

  Attributes:
      _x (float): The x-coordinate of the vector.
      _y (float): The y-coordinate of the vector.

  Methods:
      from_points(origin, dest): Create a vector from two points.
      to_dict(): Convert the vector to a dictionary.
      __add__(other): Add another vector to this vector.
      __sub__(other): Subtract another vector from this vector.
      __truediv__(other): Divide this vector by a scalar value.
      __mul__(other): Multiply this vector by a scalar value.
      mul(value): Multiply the vector by a scalar value.
      div(value): Divide the vector by a scalar value.
      add(vec): Add another vector to this vector.
      sub(vec): Subtract another vector from this vector.
      size(): Calculate the magnitude (size) of the vector.
      unit(): Get the unit vector in the same direction as this vector.
      scalar(mult): Scale the vector by a scalar value.
      x(): Get the x-coordinate of the vector.
      y(): Get the y-coordinate of the vector.
      as_tuple(): Convert the vector to a tuple.
      copy(): Create a copy of the vector.
      __eq__(other): Check if two vectors are approximately equal.
      __str__(): Get a string representation of the vector.
  """
  def __init__(self, x: float, y: float) -> None:
    """
    Initialize a Vector object.

    Args:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
    """
    super().__init__()
    self._x: float = x
    self._y: float = y
  
  @classmethod
  def from_points(cls, origin: Vector, dest: Vector) -> Vector:
    """
    Create a vector from two points.

    Args:
        origin (Vector): The origin point.
        dest (Vector): The destination point.

    Returns:
        Vector: A vector representing the difference between the destination and origin points.
    """
    x = dest.x - origin.x
    y = dest.y - origin.y

    return Vector(x, y)
  
  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the vector to a dictionary.

    Returns:
        dict: A dictionary representation of the vector.
    """
    return {
      "x": self.x,
      "y": self.y
    }

  def __add__(self, other: Vector) -> Vector:
    """
    Add another vector to this vector.

    Args:
        other (Vector): The vector to be added.

    Returns:
        Vector: The resulting vector after addition.
    """
    return self.add(other)
  
  def __sub__(self, other: Vector) -> Vector:
    """
    Subtract another vector from this vector.

    Args:
        other (Vector): The vector to be subtracted.

    Returns:
        Vector: The resulting vector after subtraction.
    """
    return self.sub(other)

  def __truediv__(self, other: float) -> Vector:
    """
    Divide this vector by a scalar value.

    Args:
        other (float): The scalar value to divide by.

    Returns:
        Vector: The resulting vector after division.
    """
    return self.div(other)

  def __mul__(self, other: float) -> Vector:
    """
    Multiply this vector by a scalar value.

    Args:
        other (float): The scalar value to multiply by.

    Returns:
        Vector: The resulting vector after multiplication.
    """
    return self.mul(other)

  def mul(self, value: Any[float, int]) -> Vector:
    """
    Multiply the vector by a scalar value.

    Args:
        value (float or int): The scalar value to multiply by.

    Returns:
        Vector: The resulting vector after multiplication.
    """
    return Vector(self.x * value, self.y * value)

  def div(self, value: Any[float, int]) -> Vector:
    """
    Divide the vector by a scalar value.

    Args:
        value (float or int): The scalar value to divide by.

    Returns:
        Vector: The resulting vector after division.
    """
    return self * (1.0 / value)

  def add(self, vec: Vector) -> Vector:
    """
    Add another vector to this vector.

    Args:
        vec (Vector): The vector to be added.

    Returns:
        Vector: The resulting vector after addition.
    """
    return Vector(self.x + vec.x, self.y + vec.y)

  def sub(self, vec: Vector) -> Vector:
    """
    Subtract another vector from this vector.

    Args:
        vec (Vector): The vector to be subtracted.

    Returns:
        Vector: The resulting vector after subtraction.
    """
    return Vector(self.x - vec.x, self.y - vec.y)

  def size(self) -> float:
    """
    Calculate the magnitude (size) of the vector.

    Returns:
        float: The magnitude of the vector.
    """
    return sqrt(self.x * self.x + self.y * self.y)

  def unit(self) -> Vector:
    """
    Get the unit vector in the same direction as this vector.

    Returns:
        Vector: The unit vector.
    """
    return self / self.size() if self.size() > 0 else Vector(self.x, self.y)
  
  def scalar(self, mult: float) -> Vector:
    """
    Scale the vector by a scalar value.

    Args:
        mult (float): The scalar value to scale the vector by.

    Returns:
        Vector: The resulting scaled vector.
    """
    return Vector(self.x * mult, self.y * mult)

  @property
  def x(self) -> float:
    """
    Get the x-coordinate of the vector.

    Returns:
        float: The x-coordinate of the vector.
    """
    return self._x
  
  @property
  def y(self) -> float:
    """
    Get the y-coordinate of the vector.

    Returns:
        float: The y-coordinate of the vector.
    """
    return self._y

  def as_tuple(self) -> Tuple[float, float]:
    """
    Convert the vector to a tuple.

    Returns:
        Tuple[float, float]: A tuple containing the x and y coordinates of the vector.
    """
    return self.x, self.y
  
  def copy(self) -> Vector:
    """
    Create a copy of the vector.

    Returns:
        Vector: A new vector with the same x and y coordinates.
    """
    return Vector(self.x, self.y)

  def __eq__(self, __o: object) -> bool:
    """
    Check if two vectors are approximately equal.

    Args:
        other (object): The object to compare to.

    Returns:
        bool: True if the vectors are approximately equal, False otherwise.
    """
    return isinstance(__o, Vector) and ( isclose(self.x, __o.x, rel_tol=1e-1) and isclose(self.y, __o.y, rel_tol=1e-1))

  def __str__(self) -> str:
    """
    Get a string representation of the vector.

    Returns:
        str: A string representation of the vector.
    """
    return f"Vec({self.x:.2f}, {self.y:.2f})"
