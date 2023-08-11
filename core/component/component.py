from typing import Any, Dict
from core.primitives import Vector


class Component(object):
  """
  Represents a base component class with properties.

  Attributes:
    properties (dict): A dictionary holding the properties of the component.

  Methods:
    to_dict(): Converts the component and its properties to a dictionary.
  """
  def __init__(self) -> None:
    self.properties = {}

  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the component and its properties to a dictionary.

    Returns:
      dict: A dictionary representation of the component.
    """
    return {}


class MetaDataComponent(Component):
  """
  Represents a component containing metadata information.

  Attributes:
    name (str): The name associated with the entity.
    type (str): The type of the entity.

  Methods:
    to_dict(): Converts the metadata component to a dictionary.
  """
  def __init__(self, name: str = '', entity_type: str = '') -> None:
    """
    Initialize a MetaDataComponent object.

    Args:
      name (str): The name associated with the entity (default is '').
      entity_type (str): The type of the entity (default is '').

    """
    super().__init__()
    self.name = name
    self.type = entity_type

  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the metadata component to a dictionary.

    Returns:
      dict: A dictionary representation of the metadata component.
    """
    return {
      "name": self.name,
      "type": self.type
    }


class MovementComponent(Component):
  """
  Represents a component related to movement information.

  Attributes:
    position (Vector): The position vector of the entity.
    velocity (Vector): The velocity vector of the entity.
    acceleration (Vector): The acceleration vector of the entity.

  Methods:
    to_dict(): Converts the movement component to a dictionary.
  """
  def __init__(self, position: Vector = Vector(0, 0)) -> None:
    """
    Initialize a MovementComponent object.

    Args:
      position (Vector): The initial position vector (default is Vector(0, 0)).

    """
    super().__init__()
    self.position:     Vector = position
    self.velocity:     Vector = Vector(0, 0)
    self.acceleration: Vector = Vector(0, 0)
    
  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the movement component to a dictionary.

    Returns:
      dict: A dictionary representation of the movement component.
    """
    return {
      "position":     self.position.to_dict(),
      "velocity":     self.velocity.to_dict(),
      "acceleration": self.acceleration.to_dict(),
    }


class EnergyComponent(Component):
  """
  Represents a component related to energy management.

  Attributes:
    max_energy (float): The maximum energy capacity.
    current (float): The current energy level.
    rate (float): The energy change rate.

  Methods:
    __str__(): Returns a string representation of the energy component.
    ratio(): Calculates the current energy ratio.
    to_dict(): Converts the energy component to a dictionary.
  """
  def __init__(self, max_energy: float = 100.0, rate: float = 0.01) -> None:
    """
    Initialize an EnergyComponent object.

    Args:
      max_energy (float): The maximum energy capacity (default is 100.0).
      rate (float): The energy change rate (default is 0.01).

    """
    super().__init__()
    self.max_energy: float = max_energy
    self.current: float = max_energy
    self.rate: float = rate

  def __str__(self) -> str:
    """
    Return a string representation of the energy component.

    Returns:
      str: A string showing the current energy level and maximum energy capacity.
    """
    return f"{int(self.current)}/{int(self.max_energy)}"

  @property
  def ratio(self) -> float:
    """
    Calculate the current energy ratio.

    Returns:
      float: The ratio of current energy level to maximum energy capacity.
    """
    return self.current / self.max_energy

  def to_dict(self) -> Dict[str, Any]:
    """
    Convert the energy component to a dictionary.

    Returns:
      dict: A dictionary representation of the energy component.
    """
    return {
      "max_energy": self.max_energy,
      "current": self.current,
      "rate": self.rate,
    }