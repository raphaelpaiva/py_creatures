from typing import Dict
from creatures.render_system.constants import FPS_LIMIT


class Stats(object):
  def __init__(self) -> None:
    self.fps_limit: int     = FPS_LIMIT
    self._frametime: float  = 0
    self.framerate: float   = 0
  
  def get_stats_dict(self) -> Dict[str, str]:
    framerate = int(self.framerate)
    framerate = framerate if framerate < 1000 else 'inf'
    return {
      'FPS Limit: ': str(self.fps_limit),
      'Frame Rate: ': f"{framerate}Hz",
      'Frame time: ': f"{self.frametime:.2f}ms",
    }
  
  def __str__(self) -> str:
    return '\n'.join([k + ' ' + v for k,v in self.get_stats_dict().items()]) + '\n'

  @property
  def frametime(self) -> float:
    return self._frametime

  @frametime.setter
  def frametime(self, value: float):
    self._frametime = value
    self.framerate = 1000 / (self.frametime + 0.00001)
