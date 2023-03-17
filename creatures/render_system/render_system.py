from collections import namedtuple

from creatures.render_system.world_widget import WorldWidget
from .stats import Stats
from tkinter import Widget
from typing import Dict, List
import pygame as pg

from creatures.component import MovementComponent
from .text_widget import TextWidget
from .constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, FPS_LIMIT, GREEN, NICE_COLOR, ORIGIN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, ZOOM_LEVEL, UIColor, UIPosition, UISize
from .widget import Widget

from creatures.world import World
from creatures.entity import Entity
from creatures.system import System


class RenderSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
    self.stats = Stats()
    self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    self.fps_limit = FPS_LIMIT
    self.widgets: List[Widget] = []
    
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

  def update(self):
    self.screen.fill(WHITE)
    self.stats.frametime = self.clock.tick(self.fps_limit)
    self.stats_widget.set_text(f"Debug\nFramerate: {min(1000.0, self.stats.framerate):4.1f} fps")
    for widget in self.widgets:
      widget.render()
    pg.display.update()
