from typing import Dict
from creatures.render_system.constants import FPS_LIMIT


class Stats(object):
  def __init__(self) -> None:
    self.fps_limit: int     = FPS_LIMIT
    self._frametime: float  = 0
    self.framerate: float   = 0
    self.dt: float          = 0
    self.update_time: float = 0
    self.render_time: float = 0
    self.total_time: float  = 0
    self.world_time         = 0
  
  def get_stats_dict(self) -> Dict[str, str]:
    return {
      'FPS Limit: ': str(self.fps_limit),
      'Frame Rate: ': f"{self.framerate:4.1f}Hz",
      'Frame time: ': f"{self.frametime:.5f}ms",
      'Update time: ': f"{self.update_time:.5f}ms",
      'Render time: ': f"{self.render_time:.5f}ms",
      'Total time: ': f"{self.total_time:.5f}ms",
      '𝚫t': f"{self.dt:.5f}",
      'World clock': f"{self.world_time:.2f}"
    }

  @property
  def frametime(self) -> float:
    return self._frametime

  @frametime.setter
  def frametime(self, value: float):
    self._frametime = value
    self.framerate = 1000 / (self.frametime + 0.00001)
    self.world_time += self.dt * 100
