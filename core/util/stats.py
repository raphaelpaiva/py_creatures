from abc import ABC, abstractmethod
from typing import Dict, Any


class Stats(ABC):
  @abstractmethod
  def get_dict(self) -> Dict[str, Any]:
    return {}
