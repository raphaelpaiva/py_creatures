from typing import Dict, List
import pygame as pg

from .world import Entity, World
from .system import System

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = SCREEN_WIDTH
ZOOM_LEVEL    = 0.8
BORDER_WIDTH  = 2

FPS_LIMIT = 0

NICE_COLOR = (128, 11, 87)
WHITE      = (255, 255, 255)
GREEN      = (10, 200, 10)
BLACK      = (0, 0, 0)

class Stats(object):
  def __init__(self) -> None:
    self.fps_limit: int     = FPS_LIMIT
    self._frametime: float  = 0
    self.framerate: float   = 0
    self.dt: float          = 0
    self.update_time: float = 0
    self.render_time: float = 0
    self.total_time: float  = 0
    self.world_time         = 0
  
  def get_stats_dict(self) -> Dict[str, str]:
    return {
      'FPS Limit: ': str(self.fps_limit),
      'Frame Rate: ': f"{self.framerate:4.1f}Hz",
      'Frame time: ': f"{self.frametime:.5f}ms",
      'Update time: ': f"{self.update_time:.5f}ms",
      'Render time: ': f"{self.render_time:.5f}ms",
      'Total time: ': f"{self.total_time:.5f}ms",
      '𝚫t': f"{self.dt:.5f}",
      'World clock': f"{self.world_time:.2f}"
    }

  @property
  def frametime(self) -> float:
    return self._frametime

  @frametime.setter
  def frametime(self, value: float):
    self._frametime = value
    self.framerate = 1000 / (self.frametime + 0.00001)
    self.world_time += self.dt * 100

class RenderSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
    self.stats = Stats()
    self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    self.zoom_level = ZOOM_LEVEL
    self.fps_limit = FPS_LIMIT
    
    pg.init()
    self.screen = pg.display.set_mode(self.screen_size)

    self.bottom_layer = pg.Surface(size=self.screen.get_size())
    self.world_layer  = pg.Surface(size=self.screen.get_size())
    self.top_layer    = pg.Surface(size=self.screen.get_size())
    self.layers = {
      'bottom': self.bottom_layer,
      'world': self.world_layer,
      'top': self.top_layer
    }

    self.font = pg.font.SysFont(None, 18)

    self.clock = pg.time.Clock()
    self.stats.frametime = self.clock.tick(self.fps_limit)
    
    self.scale = self.zoom_level * (self.screen.get_width() / self.world.width)
  
  def update(self):
    self.render()

  def render(self):
    self.stats.frametime = self.clock.tick(self.fps_limit)
    self.stats.dt = self.world.dt
    self.stats.world_time += self.stats.dt

    offset_x = 0.5 * (self.screen.get_width() - self.world.width * self.scale)
    offset_y = 0.5 * (self.screen.get_height() - self.world.height * self.scale)
    
    self.screen.fill(WHITE)
    # Draw "board"
    pg.draw.rect(
      self.screen,
      (200, 200, 200),
      pg.rect.Rect(
        0 + offset_x,
        0 + offset_y,
        self.world.width * self.scale,
        self.world.height * self.scale
      )
    )

    sorted_entities = sorted(self.world.entities(), key=lambda e: e.size, reverse=True)
    self._render_bottom_layer(offset_x, offset_y, sorted_entities)
    self._render_middle_layer(offset_x, offset_y, sorted_entities)
    self._render_top_layer(offset_x, offset_y, sorted_entities)
    pg.display.update()

  def _render_top_layer(self, offset_x, offset_y, sorted_entities):
    for entity in sorted_entities:
      border_width = 2
      size = entity.size * self.scale - border_width
    
      entity_pos = [
      entity.position.x * self.scale + offset_x,
      entity.position.y * self.scale + offset_y
    ]
    
      text_offset = [
      5 + size,
      -1 * size - 5
    ]
      name_text = self.font.render(entity.properties.get('name', entity.id), True, NICE_COLOR)
      name_pos  = [entity_pos[0] + text_offset[0], entity_pos[1] + text_offset[1]]
      self.screen.blit(name_text, name_pos)

      behavior_text = self.font.render(str(entity.behavior), True, NICE_COLOR)
      behavior_pos  = [name_pos[0], name_pos[1] + self.font.get_height()]
      self.screen.blit(behavior_text, behavior_pos)
  
    self.render_stats()

  def _render_middle_layer(self, offset_x: float, offset_y: float, sorted_entities: List[Entity]):
    for entity in sorted_entities:
      border_width = 2
      size = entity.size * self.scale - border_width
    
      entity_pos = [
        entity.position.x * self.scale + offset_x,
        entity.position.y * self.scale + offset_y
      ]
      
      if entity.is_resource:
        self._render_resource(entity, size, entity_pos)
      else:
        self._render_entity(entity, size, entity_pos)

  def _render_resource(self, entity, size, entity_pos):
    pg.draw.rect(
      self.screen,
      GREEN,
      pg.Rect(
        entity_pos[0] - size / 2,
        entity_pos[1] - size / 2,
        size,
        size,
      )
    )

    pg.draw.rect(
      self.screen,
      BLACK,
      pg.Rect(
        entity_pos[0] - size / 2,
        entity_pos[1] - size / 2,
        size,
        size,
      ),
      width=BORDER_WIDTH
    )
          
  def _render_entity(self, entity, size, entity_pos):
    pg.draw.circle(
      self.screen,
      entity.properties.get('color', NICE_COLOR),
      entity_pos,
      size
    )
      
    pg.draw.circle(
      self.screen,
      BLACK,
      entity_pos,
      size,
      width=BORDER_WIDTH
    )

  def _render_bottom_layer(self, offset_x, offset_y, sorted_entities):
    for entity in sorted_entities:
      border_width = 2
      size = entity.size * self.scale - border_width
    
      entity_pos = [
      entity.position.x * self.scale + offset_x,
      entity.position.y * self.scale + offset_y
    ]

      if 'sensor_radius' in entity.properties:
        pg.draw.circle(
        self.screen,
        (0, 0, 128),
        entity_pos,
        entity.properties['sensor_radius'] * self.scale
      )

  def render_stats(self, position: list = [10, 10]):
    y_margin = 5
    x_margin = 5

    stats = self.stats.get_stats_dict()
    text_surfaces: List[pg.Surface] = []
    box_height = 0
    box_width = 0

    for name, value in stats.items():
      text = f"{name}: {value}"
      antialias = True
      text_surface = self.font.render(
        text,
        antialias,
        NICE_COLOR
      )
      box_height += text_surface.get_height() + 2 * y_margin
      box_width = max(box_width, text_surface.get_width()) + 2 * x_margin
    
      text_surfaces.append(
        text_surface
      )

    rect = pg.draw.rect(
      surface=self.screen,
      rect=pg.Rect(position[0], position[1], box_width, box_height),
      color=(125, 125, 125)
    )

    title_surface = self.font.render('stats', True, (87, 11, 128))
    self.screen.blit(title_surface, [rect.right - x_margin - title_surface.get_width(), rect.top])

    y_offset = title_surface.get_height()
    for text_surface in text_surfaces:
      pos  = [position[0] + x_margin, position[1] + y_margin + y_offset]
      self.screen.blit(text_surface, pos)
      y_offset += y_margin + text_surface.get_height()

    