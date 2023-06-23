from typing import Optional, Union
import pygame
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIWindow, UITextBox, UILabel
from pygame import Rect

from core.render_system.stats import Stats

TEMPLATE = """
<p><b>FPS Limit:</b>{limit:.2f}</p>
<p><b>Framerate:</b>{framerate:.2f}Hz</p>
<p><b>Frame time:</b>{frametime:.2f}ms</p>
"""

class StatsWidget(UIWindow):
  def __init__(
      self,
      stats: Stats,
      rect: Rect,
      manager: IUIManagerInterface | None = None,
      window_display_title: str = "Stats",
      element_id: str | None = None,
      object_id: ObjectID | str | None = None,
      resizable: bool = True,
      visible: int = 1,
      draggable: bool = True):
    super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)
    self.stats = stats
    self.text_widget = UILabel(Rect(0,0,-1,-1), '<b>Opa</b>', self.ui_manager, self, self)
  
  def update(self, time_delta: float):
    
    return super().update(time_delta)
  
