import sys
from tkinter import font
from typing import List

import pygame as pg
import pygame.gfxdraw as gfx

from creatures.entity import Entity
from creatures.render_system.entity_widget import EntityWidget
from creatures.render_system.mouse_handler import Mouse
from creatures.render_system.style import Style
from creatures.render_system.world_widget import WorldWidget
from creatures.system import System
from creatures.world import World

from .constants import (FPS_LIMIT, GREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE,
                        ZOOM_LEVEL, UISize)
from .stats import Stats
from .text_widget import TextWidget
from .widget import Widget

mouse: Mouse = Mouse()

class RenderSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
    self.stats = Stats()
    self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    self.fps_limit = FPS_LIMIT
    self.ui_stack: List[Widget] = []
    self.mouse = mouse
    
    pg.init()
    self.screen = pg.display.set_mode(self.screen_size)
    self.font = pg.font.SysFont(None, 18)

    self.clock = pg.time.Clock()
    self.stats.frametime = self.clock.tick(self.fps_limit)

    self.zoom_level = ZOOM_LEVEL
    
    self.scale = self.zoom_level * (self.screen.get_width() / self.world.width)


    world_widget_size = UISize(
      self.world.width * self.scale,
      self.world.height * self.scale
    )
    world_widget_style = Style()
    world_widget_style.size = world_widget_size

    self.world_widget = WorldWidget(
      surface=self.screen,
      world=world,
      scale=self.scale,
      font=self.font,
      position=Widget.center_in_surface(self.screen, world_widget_size),
      style=world_widget_style
    )

    self.stats_widget = TextWidget(self.screen, 'Framerate: 0000.0 fps\nOpa!', style=Style(font=self.font))
    self.stats_widget = TextWidget(self.screen, 'Framerate: 0000.0 fps\nOpa!', style=Style(font=self.font))
    self.entity_widget = None
    
    self.add_ui_element(self.world_widget)
    self.add_ui_element(self.stats_widget)

  def update(self, entities: List[Entity]):
    if not self.entity_widget:
      self.entity_widget = EntityWidget(self.screen, entities[0], style=Style(font=self.font))
      self.add_ui_element(self.entity_widget)
    
    self.ui_stack.sort(key=lambda w: w.z_position)
    self.mouse.update_position()
    self.handle_events()
    self.screen.fill(WHITE)
    self.stats.frametime = self.clock.tick(self.fps_limit)
    self.stats_widget.set_text(str(self.stats))

    self.top_hovering_widget = None
    for widget in self.ui_stack:
      if widget.border_rect.collidepoint(self.mouse.position.as_tuple()):
        if self.top_hovering_widget is None:
          self.top_hovering_widget = widget
        elif self.top_hovering_widget.z_position < widget.z_position:
          self.top_hovering_widget = widget
      else:
        widget.hovering = False
      
      widget.render()
    
    if self.top_hovering_widget:
      self.top_hovering_widget.hovering = True
      self.top_hovering_widget.on_hover()
    
    pg.display.update()

  def draw_cursor(self):
    cursor_size = 5 * self.scale
    
    gfx.aacircle(
      self.screen,
      self.mouse.position.x,
      self.mouse.position.y,
      int(cursor_size),
      GREEN
    )

  def add_ui_element(self, element: Widget):
    element.z_position = len(self.ui_stack)
    self.ui_stack.append(element)

  def handle_events(self):
    for event in pg.event.get():
      e: pg.event.Event = event
      if e.type == pg.MOUSEBUTTONDOWN:
        if self.top_hovering_widget:
          self.ui_stack.remove(self.top_hovering_widget)
          self.add_ui_element(self.top_hovering_widget)
          for i, ui_element in enumerate(self.ui_stack):
            ui_element.z_position = i
          self.top_hovering_widget.on_mouse_down()
      if e.type == pg.MOUSEBUTTONUP:
        if self.top_hovering_widget:
          self.top_hovering_widget.on_mouse_up()
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()