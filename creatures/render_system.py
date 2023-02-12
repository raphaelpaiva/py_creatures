from collections import namedtuple
from typing import Dict, List
import pygame as pg

from .world import Entity, World
from .system import System

UIPosition = namedtuple('UIPosition', ['x', 'y'])
UISize     = namedtuple('UISize', ['width', 'height'])
UIColor    = namedtuple('ScreenColor', ['r', 'g', 'b'])

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = SCREEN_WIDTH
ZOOM_LEVEL    = 0.95
BORDER_WIDTH  = 2
WORLD_MARGIN  = 5
ORIGIN        = UIPosition(0, 0)
DEFAULT_SIZE  = UISize(SCREEN_WIDTH, SCREEN_HEIGHT)

FPS_LIMIT = 0

BACKGROUND_GREY = UIColor(200, 200, 200)
NICE_COLOR      = UIColor(128, 11, 87)
WHITE           = UIColor(255, 255, 255)
GREEN           = UIColor(10, 200, 10)
BLACK           = UIColor(0, 0, 0)

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

class SquareWidget(object):
  def __init__(self,
    surface:          pg.Surface,
    position:         UIPosition = ORIGIN,
    size:             UISize     = DEFAULT_SIZE,
    background_color: UIColor    = BACKGROUND_GREY,
    border_width:     int        = BORDER_WIDTH,
    border_color:     UIColor    = BLACK,
    margin:           int        = BORDER_WIDTH
  ) -> None:
    self.surface          = surface
    self.size             = size
    self.background_color = background_color
    self.border_width     = border_width
    self.border_color     = border_color
    self.margin           = margin
    layout_offset         = self.margin + self.border_width
    
    self.position         = UIPosition(layout_offset + position.x, layout_offset + position.y)
    self.rect             = pg.rect.Rect(
      self.position.x,
      self.position.y,
      self.size.width,
      self.size.height
    )
    
    self.border_rect  = pg.rect.Rect(
      self.rect.left - self.border_width,
      self.rect.top  - self.border_width,
      self.rect.width  + 2 * self.border_width,
      self.rect.height + 2 * self.border_width
    )
  
  def render(self):
    pg.draw.rect(
      self.surface,
      self.border_color,
      self.border_rect,
      width=self.border_width
    )

    pg.draw.rect(
      self.surface,
      self.background_color,
      self.rect,
    )

  @classmethod
  def center_in_surface(cls, surface: pg.surface, size: UISize) -> UIPosition:
    return UIPosition(
      0.5 * (surface.get_width()  - size.width),
      0.5 * (surface.get_height() - size.height)
    )

class WorldWidget(SquareWidget):
  def __init__(
    self,
    surface: pg.Surface,
    world: World,
    scale: float,
    font: pg.font.Font,
    position: UIPosition = ORIGIN,
    size: UISize = DEFAULT_SIZE,
    background_color: UIColor = BACKGROUND_GREY,
    border_width: int = BORDER_WIDTH,
    border_color: UIColor = BLACK,
    margin: int = BORDER_WIDTH
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
    self.layers = {
      'bottom': self.bottom_layer,
      'world': self.world_layer,
      'top': self.top_layer
    }
  
  def render(self):
    super().render()
    
    sorted_entities = sorted(self.world.entities(), key=lambda e: e.size, reverse=True)
    self._render_bottom_layer(sorted_entities)
    self._render_middle_layer(sorted_entities)
    self._render_top_layer(sorted_entities)

  def _render_top_layer(self, sorted_entities: List[Entity]):
    for entity in sorted_entities:
      entity_border_width = 2
      size = entity.size * self.scale - entity_border_width
    
      entity_pos = [
      entity.position.x * self.scale + self.position.x,
      entity.position.y * self.scale + self.position.y
    ]
    
      text_offset = [
      5 + size,
      -1 * size - 5
    ]
      name_text = self.font.render(entity.properties.get('name', entity.id), True, NICE_COLOR)
      name_pos  = [entity_pos[0] + text_offset[0], entity_pos[1] + text_offset[1]]
      self.surface.blit(name_text, name_pos)

      behavior_text = self.font.render(str(entity.behavior), True, NICE_COLOR)
      behavior_pos  = [name_pos[0], name_pos[1] + self.font.get_height()]
      self.surface.blit(behavior_text, behavior_pos)

  def _render_middle_layer(self, sorted_entities: List[Entity]):
    for entity in sorted_entities:
      border_width = 2
      size = entity.size * self.scale - border_width
    
      entity_pos = [
        entity.position.x * self.scale + self.position.x,
        entity.position.y * self.scale + self.position.y
      ]
      
      if entity.is_resource:
        self._render_resource(entity, size, entity_pos)
      else:
        self._render_entity(entity, size, entity_pos)

  def _render_resource(self, entity, size, entity_pos):
    pg.draw.rect(
      self.surface,
      GREEN,
      pg.Rect(
        entity_pos[0] - size / 2,
        entity_pos[1] - size / 2,
        size,
        size,
      )
    )

    pg.draw.rect(
      self.surface,
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
      self.surface,
      entity.properties.get('color', NICE_COLOR),
      entity_pos,
      size
    )
      
    pg.draw.circle(
      self.surface,
      BLACK,
      entity_pos,
      size,
      width=BORDER_WIDTH
    )

  def _render_bottom_layer(self,sorted_entities: List[Entity]):
    for entity in sorted_entities:
      entity_pos = [
        entity.position.x * self.scale + self.position.x,
        entity.position.y * self.scale + self.position.y
      ]

      if 'sensor_radius' in entity.properties:
        pg.draw.circle(
        self.surface,
        (0, 0, 128),
        entity_pos,
        entity.properties['sensor_radius'] * self.scale
      )

class RenderSystem(System):
  def __init__(self, world: World) -> None:
    super().__init__()
    self.world = world
    self.stats = Stats()
    self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    self.fps_limit = FPS_LIMIT
    self.widgets: List[SquareWidget] = []
    
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
      position=SquareWidget.center_in_surface(self.screen, world_widget_size),
      size=world_widget_size
    )

    self.widget = SquareWidget(self.screen, UIPosition(0, 0), UISize(50, 50))

    self.widgets.append(self.world_widget)
    self.widgets.append(self.widget)

  def update(self):
    self.screen.fill(WHITE)
    for widget in self.widgets:
      widget.render()
    pg.display.update()
