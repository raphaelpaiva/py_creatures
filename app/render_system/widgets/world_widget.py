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


MIN_SCALE = 1.0
MAX_SCALE = 20.0


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

    self.dragging = False
    self.log = logging.getLogger(self.__class__.__name__)
    self.world = world
    self._scale = scale
    self.original_scale = self._scale
    self.font = font
    self.bottom_layer = pg.Surface(size=self.surface.get_size())
    self.world_layer = pg.Surface(size=self.surface.get_size())
    self.top_layer = pg.Surface(size=self.surface.get_size())
    self.hover: Graphic | None = None

    self.layers = {
      'bottom': self.bottom_layer,
      'world': self.world_layer,
      'top': self.top_layer
    }
    self.graphics: List[Graphic] = self.get_graphics()

    self.view_port_position: Vector = Vector(10, 0)

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
    if self.dragging:
      self.view_port_position += mouse.relative_movement / self.scale
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
    self.dragging = False
    if self.hover:
      self.selected_entity = self.hover.entity
      self.hover.toggle_selected()
    else:
      self.selected_entity = None

  def on_mouse_down(self):
    super().on_mouse_down()
    if self.hovering:
      self.dragging = True

  def on_mouse_wheel(self, wheel_vec: Vector):
    scale_step = wheel_vec.y / 10.0
    self.scale += scale_step

  def _set_hover(self):
    mouse_position = mouse.position - self.position

    for graphic in self.graphics:
      graphic_size = graphic.size * self.scale - graphic.border_width
      graphic_pos = (self.view_port_position + graphic.position) * self.scale
      if (graphic_pos - mouse_position).size() <= graphic_size:
        self.hover = graphic
        return

    self.hover = None

  def _render_top_layer(self):
    for graphic in self.graphics:
      if graphic.layer != TOP_LAYER:
        continue

      size = graphic.size * self.scale - graphic.border_width
      graphic_pos = (self.view_port_position + graphic.position) * self.scale

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
      graphic_pos = (self.view_port_position + graphic.position) * self.scale

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
        sprite_offset = Vector(graphic.sprite.get_width(), graphic.sprite.get_height()) / 2
        sprite_position = graphic_pos - sprite_offset
        self.surface.blit(
          graphic.sprite,
          sprite_position.as_tuple()
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

  def _render_bottom_layer(self):
    for graphic in self.graphics:
      if graphic.layer != BOTTOM_LAYER:
        continue

      graphic_size = graphic.size * self.scale
      graphic_pos = (self.view_port_position + graphic.position) * self.scale

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

  def load_sprite(self, graphic: Graphic):
    try:
      graphic.sprite = pg.image.load(graphic.sprite).convert_alpha()
      graphic.original_sprite = graphic.sprite
    except Exception as e:
      self.log.warning(f"Error loading sprite: {e}. Using default shape")
      graphic.sprite = None

  @property
  def scale(self):
    return self._scale

  @scale.setter
  def scale(self, new_scale: float):
    if new_scale <= MIN_SCALE:
      self._scale = MIN_SCALE
      new_scale = MIN_SCALE
    elif new_scale >= MAX_SCALE:
      self._scale = MAX_SCALE
      new_scale = MAX_SCALE

    self._scale = new_scale
    ratio = self._scale / self.original_scale
    for g in self.get_graphics():
      if g.sprite and isinstance(g.sprite, pg.Surface):
        aspect_ratio = g.original_sprite.get_height() / g.original_sprite.get_width() * 1.0
        new_width = g.original_sprite.get_width() * ratio
        new_height = new_width * aspect_ratio
        size = (new_width, new_height)
        g.sprite = pg.transform.scale(
          g.original_sprite,
          size
        )
