import sys
from tkinter import Widget
from typing import List

import pygame as pg
import pygame.gfxdraw as gfx

from creatures.entity import Entity
from creatures.render_system.mouse_handler import Mouse
from creatures.render_system.world_widget import WorldWidget
from creatures.system import System
from creatures.world import World

from .constants import (FPS_LIMIT, GREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE,
                        ZOOM_LEVEL, UIPosition, UISize)
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
    self.widgets: List[Widget] = []
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

    self.world_widget = WorldWidget(
      surface=self.screen,
      world=world,
      scale=self.scale,
      font=self.font,
      position=Widget.center_in_surface(self.screen, world_widget_size),
      size=world_widget_size
    )

    self.stats_widget = TextWidget(self.screen, 'Framerate: 0000.0 fps\nOpa!', self.font)
    
    self.widgets.append(self.world_widget)
    self.widgets.append(self.stats_widget)

  def update(self, entities: List[Entity]):
    self.mouse.update_position()
    self.handle_events()
    self.screen.fill(WHITE)
    self.stats.frametime = self.clock.tick(self.fps_limit)
    self.stats_widget.set_text(str(self.stats))

    for widget in self.widgets:
      widget.render()
    
    self.draw_cursor()
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

  def handle_events(self):
    for event in pg.event.get():
      e: pg.event.Event = event
      if e.type == pg.MOUSEBUTTONDOWN:
        for widget in self.widgets:
          widget.on_mouse_down()
      if e.type == pg.MOUSEBUTTONUP:
        for widget in self.widgets:
          widget.on_mouse_up()
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()