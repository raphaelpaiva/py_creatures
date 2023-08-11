import logging
from typing import List
import pygame as pg

from creatures.app.render_system.graphics import Graphic, SimpleGraphicComponent
from creatures.core.primitives import Vector

from creatures.app.render_system.constants import BOTTOM_LAYER, MIDDLE_LAYER, ORIGIN, TOP_LAYER
from creatures.app.render_system.style import Style
from creatures.app.render_system.widgets.widget import Widget
from creatures.core.world import World

from creatures.app.render_system.mouse_handler import mouse


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
    self.hover: Graphic | None = None

    self.layers = [BOTTOM_LAYER, MIDDLE_LAYER, TOP_LAYER]
    self.graphics: List[Graphic] = self.get_graphics()

    self.view_port_position: Vector = Vector(0, 0)

    self.movable = False

    self.selected_entity = None

  def get_graphics(self):
    result: List[Graphic] = []
    for entity in sorted(self.world.entities(), key=lambda e: e.size, reverse=True):
      graphic_component = entity.get_component(SimpleGraphicComponent)
      if not graphic_component:
        graphic_component = SimpleGraphicComponent(entity, self.scale)
        entity.add_component(graphic_component)

      result.extend(graphic_component.graphics)

    return result

  def update(self):
    if self.dragging:
      self.view_port_position += mouse.relative_movement / self.scale
    self.graphics = self.get_graphics()
    self._set_hover()
    self.draw()

  def draw(self):
    for layer in self.layers:
      for graphic in self.graphics:
        graphic_pos = (self.view_port_position + graphic.position) * self.scale
        if graphic.layer == layer:
          graphic.scale(self.scale)
          graphic_surface = graphic.render()

          anchor_offset = graphic.anchor()
          graphic_position = graphic_pos - anchor_offset + graphic.style.offset * self.scale

          self.surface.blit(
            graphic_surface,
            graphic_position.as_tuple()
          )

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
      graphic_size = graphic.entity.size * self.scale - graphic.style.border_width
      graphic_pos = (self.view_port_position + graphic.position) * self.scale
      if (graphic_pos - mouse_position).size() <= graphic_size:
        self.hover = graphic
        return

    self.hover = None

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

    for g in self.get_graphics():
      g.scale(self._scale)