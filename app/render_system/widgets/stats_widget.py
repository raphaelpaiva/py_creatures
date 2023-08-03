import pygame as pg
from core.primitives import Vector
from app.render_system.constants import ORIGIN
from core.util import Stats
from .style import Style
from .text_widget import TextWidget


class StatsWidget(TextWidget):
  def __init__(self,
               surface: pg.Surface,
               header: str,
               stats: Stats,
               position: Vector = ORIGIN,
               style: Style = Style()
               ) -> None:
    self.stats = stats
    self.header = header
    self.stats_text = f"{self.header}\n{self.dump()}"
    super().__init__(surface, self.stats_text, position=position, style=style)

  def update(self):
    self.stats_text = f"{self.header}\n{self.dump()}"
    self.set_text(self.stats_text)
    super().update()

  def dump(self) -> str:
    if self.stats:
      return "\n".join([f"{k}: {v}" for k, v in self.stats.get_dict().items()])
    else:
      return 'No stats'
