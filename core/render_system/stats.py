from typing import Dict
from core.render_system.constants import FPS_LIMIT


class Stats(object):
  def __init__(self) -> None:
    self.fps_limit: int          = FPS_LIMIT
    self._frametime: float       = 0
    self.framerate: float        = 0
    self.framerate_acc: float    = 0
    self.frametime_acc: float    = 0
    self.readings_counter: float = 0
  
  def get_stats_dict(self) -> Dict[str, str]:
    framerate = int(self.framerate)
    framerate = f"{framerate}Hz" if framerate < 1000 else '+inf'
    return {
      'FPS Limit: ': str(self.fps_limit),
      'Frame Rate: ': framerate,
      'Avg Frame Rate: ': f"{self.avg_framerate:.2f}Hz",
      'Frame Time: ': f"{self.frametime:.2f}ms",
      'Avg Frame Time: ': f"{self.avg_frametime:.2f}ms",
    }
  
  def __str__(self) -> str:
    return '\n'.join([k + ' ' + v for k,v in self.get_stats_dict().items()])

  @property
  def frametime(self) -> float:
    return self._frametime

  @frametime.setter
  def frametime(self, value: float):
    self._frametime = value
    self.framerate = 1000 / (self.frametime + 0.00001)
    self.frametime_acc += self.frametime
    self.readings_counter += 1
  
  @property
  def avg_framerate(self) -> float:
    return 1000 / (self.avg_frametime + 0.00001)

  @property
  def avg_frametime(self) -> float:
    return self.frametime_acc / self.readings_counter
