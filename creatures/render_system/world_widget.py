from typing import List, Set
import pygame as pg
import pygame.gfxdraw as gfx
from . import render_system
from creatures.render_system.graphics import SimpleGraphicComponent
from creatures.primitives import Vector

from creatures.render_system.aux_types import UIColor, UIPosition, UISize
from creatures.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, GREEN, NICE_COLOR, ORIGIN, WHITE
from creatures.render_system.widget import Widget
from creatures.world import World

class WorldWidget(Widget):
  def __init__(
    self,
    surface: pg.Surface,
    world: World,
    scale: float,
    font: pg.font.Font,
    position: UIPosition      = ORIGIN,
    size: UISize              = DEFAULT_SIZE,
    background_color: UIColor = BACKGROUND_GREY,
    border_width: int         = BORDER_WIDTH,
    border_color: UIColor     = BLACK,
    margin: int               = BORDER_WIDTH
  ) -> None:

    super().__init__(
      surface,
      position,
      size,
      background_color,
      border_width,
      border_color,
      margin
    )
    
    self.world = world
    self.scale = scale
    self.font = font
    self.bottom_layer = pg.Surface(size=self.surface.get_size())
    self.world_layer  = pg.Surface(size=self.surface.get_size())
    self.top_layer    = pg.Surface(size=self.surface.get_size())
    self.hover        = None
    self.layers = {
      'bottom': self.bottom_layer,
      'world': self.world_layer,
      'top': self.top_layer
    }
    self.graphics: List[SimpleGraphicComponent] = [e.get_component(SimpleGraphicComponent) for e in sorted(self.world.entities(), key=lambda e: e.size, reverse=True)]
  
  def update(self):
    self.graphics = [e.get_component(SimpleGraphicComponent) for e in sorted(self.world.entities(), key=lambda e: e.size, reverse=True)]
    self._set_hover()
    self._render_bottom_layer()
    self._render_middle_layer()
    self._render_top_layer()

  def on_hover(self):
    self._set_hover()
  
  def on_mouse_up(self):
    if self.hover:
      self.hover.toggle_selected()

  def _set_hover(self):
    mouse_position = render_system.mouse.position - self.position
    
    for graphic in self.graphics:
      graphic_size = graphic.size * self.scale - graphic.border_width
      graphic_pos = graphic.position * self.scale + self.position
      if ( (graphic_pos - mouse_position).size() <= graphic_size ):
        self.hover = graphic
        if render_system.mouse.is_up:
          graphic.toggle_selected()

        return
    
    self.hover = None

  def _render_top_layer(self):
    for graphic in self.graphics:
      size = graphic.size * self.scale - graphic.border_width
      graphic_pos = graphic.position * self.scale + self.position
      
      if graphic.text:
        text_offset = Vector(5 + size, -1 * size - 5)
        text_offset = self._render_text(graphic_pos, text_offset, graphic.text[0])
      
        if self.hover is graphic or graphic.selected:
          for text in graphic.text[1::]:
            text_offset = self._render_text(graphic_pos, text_offset, text)

  def _render_text(self, graphic_pos, text_offset, text):
    rendered = self.font.render(text, True, NICE_COLOR)
    text_position = graphic_pos + text_offset
    self.surface.blit(rendered, text_position.as_tuple())
    text_offset += Vector(0, self.font.get_height())
    return text_offset

  def _render_middle_layer(self):
    for graphic in self.graphics:
      graphic_size = graphic.size * self.scale - graphic.border_width
      graphic_pos = graphic.position * self.scale + self.position

      if self.hover is graphic or graphic.selected:
        graphic_color = WHITE
      else: 
        graphic_color = pg.colordict.THECOLORS.get(graphic.color) if isinstance(graphic.color, str) else graphic.color

      if graphic.shape == 'circle':
        gfx.filled_circle(
          self.surface,
          int(graphic_pos.x),
          int(graphic_pos.y),
          int(graphic_size),
          graphic_color
        )
        gfx.aacircle(
          self.surface,
          int(graphic_pos.x),
          int(graphic_pos.y),
          int(graphic_size),
          BLACK
        )
      elif graphic.shape == 'rect':
        pg.draw.rect(
          self.surface,
          GREEN,
          pg.Rect(
            graphic_pos.x - graphic_size / 2,
            graphic_pos.y - graphic_size / 2,
            graphic_size,
            graphic_size,
          )
        )

        pg.draw.rect(
          self.surface,
          BLACK,
          pg.Rect(
            graphic_pos.x - graphic_size / 2,
            graphic_pos.y - graphic_size / 2,
            graphic_size,
            graphic_size,
          ),
          width=graphic.border_width
        )

  def _render_bottom_layer(self):
    for graphic in self.graphics:
      graphic_pos  = graphic.position * self.scale + self.position

      if 'sensor_radius' in graphic.entity.properties:
        graphic_size = graphic.entity.properties['sensor_radius'] * self.scale
        gfx.aacircle(
          self.surface,
          int(graphic_pos.x),
          int(graphic_pos.y),
          int(graphic_size),
          BLACK
        )
      
      if 'grab_radius' in graphic.entity.properties:
        graphic_size = graphic.entity.properties['grab_radius'] * self.scale
        gfx.aacircle(
          self.surface,
          int(graphic_pos.x),
          int(graphic_pos.y),
          int(graphic_size),
          GREEN
        )
        
