import pygame as pg
from creatures.render_system.aux_types import UIColor, UIPosition, UISize
from creatures.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, NICE_COLOR, ORIGIN
from creatures.render_system.widget import Widget


class TextWidget(Widget):
  def __init__(self, surface: pg.Surface, text: str, font: pg.font.Font, position: UIPosition = ORIGIN, size: UISize = DEFAULT_SIZE, background_color: UIColor = BACKGROUND_GREY, border_width: int = BORDER_WIDTH, border_color: UIColor = BLACK, margin: int = BORDER_WIDTH) -> None:
    self.text = text
    self.font = font
    self.text_surface = self.font.render(self.text, True, NICE_COLOR)
    new_size = UISize(self.text_surface.get_width() + margin + border_width, self.text_surface.get_height() + margin + border_width)
    super().__init__(surface, position, new_size, background_color, border_width, border_color, margin)
  
  def update(self):
    self.surface.blit(self.text_surface, self.position)

