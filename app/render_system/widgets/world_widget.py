import logging
from pathlib import Path
from typing import List
import pygame as pg
import pygame.gfxdraw as gfx

from app.render_system.graphics import Graphic, SimpleGraphicComponent
from core.primitives import Vector

from app.render_system.constants import BLACK, BOTTOM_LAYER, GREEN, MIDDLE_LAYER, NICE_COLOR, ORIGIN, TOP_LAYER, WHITE
from app.render_system.widgets.style import Style
from app.render_system.widgets.widget import Widget
from core.world import World

from app.render_system.mouse_handler import mouse


class WorldWidget(Widget):
  def __init__(
    self,
    surface: pg.Surface,
    world: World,
    scale: float,
    font: pg.font.Font,
    position: Vector = ORIGIN,
    style: Style = Style()
  ) -> None:

    super().__init__(
      surface,
      position,
      style
    )

    self.log = logging.getLogger(self.__class__.__name__)
    self.world = world
    self._scale = scale
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
    self.graphics: List[Graphic] = self.get_graphics()
    self.movable = False

    self.selected_entity = None

  def get_graphics(self):
      graphic_components: List[SimpleGraphicComponent] = [
        e.get_component(SimpleGraphicComponent) for e in sorted(
          self.world.entities(), key=lambda e: e.size, reverse=True
        )
      ]
      result: List[Graphic] = []

      for sgc in graphic_components:
        result.extend(sgc.graphics)

      return result

  def update(self):
    self.graphics = self.get_graphics()
    self._set_hover()
    self._render_bottom_layer()
    self._render_middle_layer()
    self._render_top_layer()

  def on_hover(self):
    super().on_hover()
    self._set_hover()

  def on_mouse_up(self):
    super().on_mouse_up()
    if self.hover:
      self.selected_entity = self.hover.entity
      self.hover.toggle_selected()
    else:
      self.selected_entity = None

  def _set_hover(self):
    mouse_position = mouse.position - self.position

    for graphic in self.graphics:
      graphic_size = graphic.size * self.scale - graphic.border_width
      graphic_pos = graphic.position * self.scale
      if ( (graphic_pos - mouse_position).size() <= graphic_size ):
        self.hover = graphic
        return

    self.hover = None

  def _render_top_layer(self):
    for graphic in self.graphics:
      if graphic.layer != TOP_LAYER: continue

      size = graphic.size * self.scale - graphic.border_width
      graphic_pos = graphic.position * self.scale

      if graphic.text:
        text_offset = Vector(5 + size, -1 * size - 5)
        for text in graphic.text:
          text_offset = self._render_text(graphic_pos, text_offset, text)

  def _render_text(self, graphic_pos, text_offset, text):
    rendered = self.font.render(text, True, WHITE)
    text_position = graphic_pos + text_offset
    self.surface.blit(rendered, text_position.as_tuple())
    text_offset += Vector(0, self.font.get_height())
    return text_offset

  def _render_middle_layer(self):
    for graphic in self.graphics:
      if graphic.layer != MIDDLE_LAYER: continue

      graphic_size = graphic.size * self.scale
      graphic_pos = graphic.position * self.scale

      if self.hover is graphic or graphic.selected:
        graphic_color = WHITE
      else:
        if isinstance(graphic.color, str):
          graphic_color = pg.colordict.THECOLORS.get(graphic.color)
          if not graphic_color:
            graphic_color = pg.Color(graphic.color)
        else:
          graphic_color = graphic.color

      if graphic.sprite:
        if not graphic.converted:
          graphic.original_sprite = graphic.original_sprite.convert_alpha()
        self.surface.blit(
          graphic.sprite,
          (int(graphic_pos.x - graphic.sprite.get_width() / 2), int(graphic_pos.y - graphic.sprite.get_height() / 2))
        )
      elif graphic.shape == 'circle':
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
          graphic_color,
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

  def load_sprite(self, graphic: Graphic):
    try:
      graphic.sprite = pg.image.load(graphic.sprite).convert_alpha()
      graphic.original_sprite = graphic.sprite
    except Exception as e:
      self.log.warning(f"Error loading sprite: {e}. Using default shape")
      graphic.sprite = None

  def _render_bottom_layer(self):
    for graphic in self.graphics:
      if graphic.layer != BOTTOM_LAYER: continue

      graphic_size = graphic.size * self.scale
      graphic_pos  = graphic.position * self.scale#  + self.position

      if graphic.shape == 'circle':
        if graphic.color != 'transparent':
          graphic_color = pg.colordict.THECOLORS.get(graphic.color) if isinstance(graphic.color, str) else graphic.color
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
          graphic.border_color
        )

  @property
  def scale(self):
    return self._scale

  @scale.setter
  def scale(self, new_scale: float):
    factor = new_scale / self._scale
    self._scale = new_scale
    for g in self.get_graphics():
      if g.sprite and isinstance(g.sprite, pg.Surface):
        g.sprite = pg.transform.scale(g.original_sprite, (g.sprite.get_width() * factor, g.sprite.get_height() * factor))


