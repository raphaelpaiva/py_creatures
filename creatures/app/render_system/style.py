import pygame as pg

from creatures.app.render_system.aux_types import UIColor, UISize
from creatures.app.render_system.constants import BLACK, BORDER_WIDTH, DEFAULT_SIZE, ORIGIN
from creatures.core.primitives import Vector


class Style(object):
  def __init__(self,
               size: UISize | int | float = DEFAULT_SIZE,
               background_color: UIColor | pg.Color = pg.Color('#9D745D'),
               border_width: int = BORDER_WIDTH,
               border_color:  UIColor | pg.Color = pg.Color('#9D745D'),
               margin: int = BORDER_WIDTH,
               hover_color: UIColor | pg.Color = pg.Color('#DCCAAF'),
               font: pg.font.Font = None,
               color: UIColor | pg.Color = BLACK,
               offset: Vector = ORIGIN
               ) -> None:
    self.size = size
    self.background_color = background_color
    self.border_width = border_width
    self.border_color = border_color
    self.margin = margin
    self.hover_color = hover_color
    self.font: pg.font.Font = font
    self.color = color
    self.offset = offset
