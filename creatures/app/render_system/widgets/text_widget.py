from typing import List
import pygame as pg
from creatures.app.render_system.aux_types import UISize
from creatures.app.render_system.constants import ORIGIN
from creatures.app.render_system.style import Style
from .widget import Widget
from creatures.core.primitives import Vector


class TextWidget(Widget):
  def __init__(self, surface: pg.Surface, text: str, position: Vector = ORIGIN, style: Style = Style()) -> None:
    self.font:          pg.font.Font = style.font
    self.style:         Style = style
    self.width:         float = 0
    self.text:          str = text
    self.lines:         List[str] = []
    self.text_surfaces: List[pg.Surface] = []
    
    self.style.size = self.create_text_content(text)
    super().__init__(surface, position=position, style=self.style)

  def create_text_content(self, text):
      self.text = text
      self.lines = self.text.split('\n')
      self.text_surfaces: List[pg.Surface] = []

      self.width = 0
      height = (len(self.lines) + 1) * self.font.get_height()
      for line in self.lines:
        text_surface = self.font.render(line, True, self.style.color)
        self.width = max(self.width, text_surface.get_width())
        self.text_surfaces.append(text_surface)
      
      new_size = UISize(self.width + self.style.margin + self.style.border_width, height + self.style.margin + self.style.border_width)
      return new_size
  
  def update(self):
    text_surface_position = Vector(0, 0)
    
    for text_surface in self.text_surfaces:
      self.surface.blit(text_surface, text_surface_position.as_tuple())
      text_surface_position += Vector(0, self.font.get_height())

  def set_text(self, new_text):
    self.style.size = self.create_text_content(new_text)
    self.surface = pg.Surface(self.style.size)
    self.surface.fill(self.style.background_color)
    self.rect = self.surface.get_rect()
    self.border_rect = pg.rect.Rect(
      self.position.x + self.rect.left - self.style.border_width,
      self.position.y + self.rect.top - self.style.border_width,
      self.rect.width + 2 * self.style.border_width,
      self.rect.height + 2 * self.style.border_width
    )