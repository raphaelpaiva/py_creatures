import pygame as pg

from creatures.primitives import Vector
from . import render_system
from creatures.render_system.aux_types import UIColor, UISize
from creatures.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, ORIGIN, WHITE


class Widget(object):
  def __init__(self,
    parent:           pg.Surface,
    position:         Vector = ORIGIN,
    size:             UISize     = DEFAULT_SIZE,
    background_color: UIColor    = BACKGROUND_GREY,
    border_width:     int        = BORDER_WIDTH,
    border_color:     UIColor    = BLACK,
    margin:           int        = BORDER_WIDTH
  ) -> None:
    self.parent           = parent
    self.size             = size
    self.background_color = background_color
    self.border_width     = border_width
    self.border_color     = border_color
    self.margin           = margin
    layout_offset         = self.margin + self.border_width
    
    self._position         = Vector(layout_offset + position.x, layout_offset + position.y)
    self.surface          = pg.Surface(size)
    self.rect             = self.surface.get_rect()
    
    self.border_rect  = pg.rect.Rect(
      self.position.x + self.rect.left - self.border_width,
      self.position.y + self.rect.top  - self.border_width,
      self.rect.width  + 2 * self.border_width,
      self.rect.height + 2 * self.border_width
    )

    self.moving   = False
    self.hovering = False
    self.movable  = True
  
  def render(self):
    pg.draw.rect(
      self.parent,
      self.border_color,
      self.border_rect,
      width=self.border_width
    )

    self.surface.fill(self.background_color)

    self.update()
    if self.border_rect.collidepoint((render_system.mouse.position.x, render_system.mouse.position.y)):
      self.hovering = True
      self.on_hover()
    else:
      self.hovering = False

    if self.moving:
      self.position += render_system.mouse.relative_movement

    self.parent.blit(self.surface, self.position.as_tuple())

  def update(self): pass
  def on_mouse_up(self):
    self.moving = False
  def on_mouse_down(self):
    if self.hovering and self.movable:
      self.moving = True
  def on_hover(self):
    pg.draw.rect(
      self.parent,
      WHITE,
      self.border_rect,
      width=self.border_width
    )

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
      self.position.x + self.rect.left - self.border_width,
      self.position.y + self.rect.top  - self.border_width,
      self.rect.width  + 2 * self.border_width,
      self.rect.height + 2 * self.border_width
    )
