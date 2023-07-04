

import pygame as pg

from core.primitives import Vector
from app.render_system.aux_types import UISize
from app.render_system.constants import (ORIGIN)
from .style import Style

from ..mouse_handler import mouse

class Widget(object):
  def __init__(self,
    parent:   pg.Surface,
    position: Vector = ORIGIN,
    style:    Style = Style()
  ) -> None:
    self.parent   = parent
    self.style    = style
    layout_offset = self.style.margin + self.style.border_width
    
    self._position = Vector(layout_offset + position.x, layout_offset + position.y)
    self.surface   = pg.Surface(self.style.size)
    self.rect      = self.surface.get_rect()
    
    self.border_rect  = pg.rect.Rect(
      self.position.x + self.rect.left - self.style.border_width,
      self.position.y + self.rect.top  - self.style.border_width,
      self.rect.width  + 2 * self.style.border_width,
      self.rect.height + 2 * self.style.border_width
    )

    self.moving   = False
    self.hovering = False
    self.movable  = True

    self.z_position = -1
  
  def render(self):
    pg.draw.rect(
      self.parent,
      self.style.border_color if not self.hovering else self.style.hover_color,
      self.border_rect,
      width=self.style.border_width
    )

    self.surface.fill(self.style.background_color)

    self.update()

    if self.moving:
      self.position += mouse.relative_movement

    self.parent.blit(self.surface, self.position.as_tuple())

  def update(self): pass
  def on_mouse_up(self):
    self.moving = False
  def on_mouse_down(self):
    if self.hovering and self.movable:
      self.moving = True
  def on_hover(self): pass

  @classmethod
  def center_in_surface(cls, surface: pg.surface, size: UISize) -> Vector:
    return Vector(
      0.5 * (surface.get_width()  - size.width),
      0.5 * (surface.get_height() - size.height)
    )
  
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, new_position: Vector):
    self._position = new_position
    self.rect = self.surface.get_rect()
    self.border_rect  = pg.rect.Rect(
      self.position.x + self.rect.left - self.style.border_width,
      self.position.y + self.rect.top  - self.style.border_width,
      self.rect.width  + 2 * self.style.border_width,
      self.rect.height + 2 * self.style.border_width
    )
