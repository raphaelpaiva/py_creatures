import pygame as pg

from app.render_system.aux_types import UIColor, UISize
from app.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, WHITE


class Style(object):
  def __init__(self,
               size: UISize = DEFAULT_SIZE,
               background_color: UIColor | pg.Color = pg.Color('#9D745D'),
               border_width: int = BORDER_WIDTH,
               border_color: UIColor = pg.Color('#9D745D'),
               margin: int = BORDER_WIDTH,
               hover_color: UIColor = pg.Color('#DCCAAF'),
               font: pg.font.Font = None,
               color: UIColor | pg.Color = BLACK
               ) -> None:
    self.size = size
    self.background_color = background_color
    self.border_width = border_width
    self.border_color = border_color
    self.margin = margin
    self.hover_color = hover_color
    self.font: pg.font.Font = font
    self.color = color
