import sys
from typing import List

import pygame as pg
import pygame.gfxdraw as gfx

from core.entity import Entity
from core.primitives import Vector
from app.render_system.widgets import EntityWidget, WorldWidget, Widget, Style
from app.render_system.widgets.text_widget import TextWidget
from core.system import System
from core.world import World
from .constants import (FPS_LIMIT, GREEN, ORIGIN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE,
                        UISize, WORLD_MARGIN)
from .mouse_handler import mouse
from .stats import Stats


class RenderSystem(System):
  def __init__(self, world: World, app) -> None:
    super().__init__()
    self.top_hovering_widget = None
    self.world = world
    self.stats = Stats()
    self.screen_size = Vector(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.fps_limit = FPS_LIMIT
    self.ui_stack: List[Widget] = []
    self.mouse = mouse
    self.app = app
    
    pg.init()
    self.screen = pg.display.set_mode(self.screen_size.as_tuple())
    self.font = pg.font.SysFont('monospace', 18)

    self.clock = pg.time.Clock()
    self.stats.frametime = self.clock.tick(self.fps_limit)

    self.zoom_level = 0.7
    
    self.scale = self.zoom_level * (self.screen.get_width() / self.world.width)
    scale_x = self.scale
    scale_y = self.zoom_level * (self.screen.get_height() / self.world.height)

    world_widget_size = UISize(
      self.world.width * scale_x,
      (self.world.height + 80) * scale_y
    )
    world_widget_style = Style()
    world_widget_style.size = world_widget_size

    self.world_widget = WorldWidget(
      surface=self.screen,
      world=world,
      scale=self.scale,
      font=self.font,
      position=ORIGIN,
      style=world_widget_style,
    )
    
    self.stats_widget = TextWidget(
      self.screen, 'Framerate: 0000.0 fps\nplaceholder\nplaceholder\nplaceholder\nplaceholder',
      position=Vector(self.world_widget.position.x + self.world_widget.style.size.width + WORLD_MARGIN, 0),
      style=Style(font=self.font)
    )
    self.entity_widget = EntityWidget(
      self.screen,
      None,
      position=Vector(
        self.world_widget.position.x + self.world_widget.style.size.width + WORLD_MARGIN,
        WORLD_MARGIN + self.stats_widget.position.y + self.stats_widget.style.size.height
      ),
      style=Style(font=self.font)
    )
    self.add_ui_element(self.entity_widget)
    
    self.add_ui_element(self.world_widget)
    self.add_ui_element(self.stats_widget)

  def update(self, entities: List[Entity]):
    self.entity_widget.entity = self.world_widget.selected_entity
    
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
      if e.type == pg.KEYUP:
        if e.key == pg.K_ESCAPE:
          pg.quit()
          sys.exit()
        if e.key == pg.K_r:
          self.app.reset()
        if e.key == pg.K_EQUALS:
          self.world_widget.scale *= 2
        if e.key == pg.K_MINUS:
          self.world_widget.scale /= 2
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
