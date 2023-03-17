from typing import List
import pygame as pg
from creatures.render_system.aux_types import UIColor, UIPosition, UISize
from creatures.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, NICE_COLOR, ORIGIN
from creatures.render_system.widget import Widget
from creatures.primitives import Vector

class TextWidget(Widget):
  def __init__(self, surface: pg.Surface, text: str, font: pg.font.Font, position: UIPosition = ORIGIN, size: UISize = DEFAULT_SIZE, background_color: UIColor = BACKGROUND_GREY, border_width: int = BORDER_WIDTH, border_color: UIColor = BLACK, margin: int = BORDER_WIDTH) -> None:
    self.font = font
    self.width = 0
    
    new_size = self.create_text_content(text, border_width, margin)
    super().__init__(surface, position, new_size, background_color, border_width, border_color, margin)

  def create_text_content(self, text, border_width, margin):
      self.text = text
      self.lines = self.text.split('\n')
      self.text_surfaces: List[pg.Surface] = []

      self.width = 0
      height = len(self.lines) * self.font.get_height()
      for line in self.lines:
        text_surface = self.font.render(line, True, NICE_COLOR)
        self.width = max(self.width, text_surface.get_width())
        self.text_surfaces.append(text_surface)
      
      new_size = UISize(self.width + margin + border_width, height + margin + border_width)
      return new_size
  
  def update(self):
    text_surface_position = Vector(*self.position)
    for index, text_surface in enumerate(self.text_surfaces):
      text_surface_position += Vector(0, index * self.font.get_height())
      self.surface.blit(text_surface, text_surface_position.as_tuple())

  def set_text(self, new_text):
    self.size        = self.create_text_content(new_text, self.border_width, self.margin)
    self.surface     = pg.Surface(self.size)
    self.rect        = self.surface.get_rect()
    self.border_rect = pg.rect.Rect(
      self.position.x + self.rect.left - self.border_width,
      self.position.y + self.rect.top  - self.border_width,
      self.rect.width  + 2 * self.border_width,
      self.rect.height + 2 * self.border_width
    )