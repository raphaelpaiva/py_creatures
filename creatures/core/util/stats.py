from abc import ABC, abstractmethod
from typing import Dict, Any


class Stats(ABC):
  """
  Abstract base class for representing statistics.

  Methods:
      get_dict(): Get a dictionary representation of the statistics.
  """
  @abstractmethod
  def get_dict(self) -> Dict[str, Any]:
    """
    Get a dictionary representation of the statistics.

    This method should be overridden by subclasses to provide the specific statistics.

    Returns:
        dict: A dictionary containing the statistics data.
    """
    return {}
