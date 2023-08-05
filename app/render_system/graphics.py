import logging
from math import sqrt
from typing import Any, Dict, List, Callable
from abc import abstractmethod, ABC

import pygame.image
from pathlib import Path

from pygame import Color

from app.render_system.style import Style
from core.random_generator import generator as random
from core.component.component import Component, EnergyComponent
from app.desire.desire_abstract import DesireComponent
from core.entity import Entity
from core.primitives import Vector
from app.render_system.constants import BLACK, BOTTOM_LAYER, GREEN, MIDDLE_LAYER, TOP_LAYER, WHITE
from app.sensor.sensor import RadialSensor
from app.sensor.sensor_component import SensorComponent

TRANSPARENT = pygame.Color(0, 0, 0, 0)


def default_text_style() -> Style:
  return Style(
    color=WHITE,
    background_color=TRANSPARENT,
    font=pygame.font.SysFont('monospace', 15),
    offset=Vector(5, 0)
  )


class SimpleGraphicComponent(Component):
  def __init__(self, entity: Entity, original_scale: float = 1.0) -> None:
    super().__init__()
    self.log = logging.getLogger(self.__class__.__name__)
    self.entity = entity
    self.graphics: List[Graphic] = []
    self.original_scale = original_scale
    self.selected = False
    self.style = Style(
      size=self.entity.size,
      color=pygame.Color(self.entity.properties.get('color', 'blue')),
      border_color=pygame.Color(0, 0, 0),
    )
    try:
      self.graphics.append(
        SpriteGraphic(self.entity, self.style, MIDDLE_LAYER, self.original_scale)
      )
    except Exception as e:
      self.log.warning(f"Couldn't load sprite: {e}")
      self.graphics.append(CircleGraphic(self.entity, self.style, MIDDLE_LAYER))

    sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
    if sensor_component:
      for sensor in sensor_component.sensors:
        if isinstance(sensor, RadialSensor):
          sensor_style = Style(
            size=sensor.radius,
            color=TRANSPARENT,
            border_color=BLACK,
            border_width=1
          )
          self.graphics.append(
            CircleGraphic(self.entity, sensor_style, BOTTOM_LAYER)
          )
    if 'grab_radius' in self.entity.properties:
      graphic_size = self.entity.properties['grab_radius']
      grab_style = Style(
        size=graphic_size,
        color=TRANSPARENT,
        border_color=GREEN,
        border_width=1
      )
      self.graphics.append(
        CircleGraphic(self.entity, grab_style, BOTTOM_LAYER)
      )
  
    self.graphics.append(TextGraphic(self.entity, default_text_style(), TOP_LAYER))
    self.graphics.append(VectorGraphic(self.entity, lambda: self.entity.movement.velocity, Style(), TOP_LAYER))
  
  def toggle_selected(self):
    self.selected = not self.selected
    for graphic in self.graphics:
      graphic.selected = not graphic.selected
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      'entity': self.entity.id,
      'graphics': [g.to_dict() for g in self.graphics]
    }


class Graphic(ABC):
  def __init__(self, entity: Entity, style: Style = Style(), layer: int = MIDDLE_LAYER) -> None:
    self.entity = entity
    self.style = style
    self.shape: str = 'rect' if self.entity.is_resource else 'circle'
    self.color = self.style.color
    self.size = self.style.size
    self.border_width = self.style.border_width
    self.border_color = self.style.border_color
    self.layer = layer
    self.surface = None

    self.selected = False

  @property
  def position(self) -> Vector:
    return self.entity.movement.position

  @property
  def graphics_component(self) -> SimpleGraphicComponent:
    return self.entity.get_component(SimpleGraphicComponent)

  @abstractmethod
  def render(self) -> pygame.Surface:
    pass

  @abstractmethod
  def scale(self, new_scale):
    pass

  def anchor(self) -> Vector:
    if self.surface:
      return Vector(self.surface.get_width(), self.surface.get_height()) / 2
    else:
      return Vector(0, 0)

  def toggle_selected(self):
    if self.graphics_component:
      self.graphics_component.toggle_selected()

  def to_dict(self):
    return {
      'type': self.__class__.__name__,
      'entity': self.entity.id,
      'shape': self.shape,
      'color': self.color,
      'size': self.size,
      'border_width': self.border_width,
      'border_color': self.border_color,
      'layer': self.layer,
      'selected': self.selected
    }

  def __str__(self):
    return f"{self.__class__.__name__}({self.entity.name})"


class CircleGraphic(Graphic):
  def __init__(self, entity: Entity, style: Style = Style(), layer: int = MIDDLE_LAYER):
    super().__init__(entity, style=style, layer=layer)
    self._scale = 1.0
    self.surface = None
    self.draw()

  @property
  def radius(self):
    return self.style.size * self._scale

  def render(self) -> pygame.Surface:
    if self.surface:
      return self.surface
    else:
      self.draw()
      return self.surface

  def scale(self, new_scale):
    if self._scale != new_scale:
      self._scale = new_scale
      self.surface = None

  def draw(self):
    if not self.surface:
      surface_size = Vector(self.radius, self.radius) * 2
      self.surface = pygame.Surface(surface_size.as_tuple()).convert_alpha()

    self.surface.fill(TRANSPARENT)
    # filled
    pygame.draw.circle(
      surface=self.surface,
      color=self.style.color,
      center=(self.surface.get_width() / 2, self.surface.get_height() / 2),
      radius=int(self.radius - self.style.border_width),
    )

    # border
    pygame.draw.circle(
      surface=self.surface,
      color=self.style.border_color,
      center=(self.surface.get_width() / 2, self.surface.get_height() / 2),
      radius=int(self.radius),
      width=self.style.border_width
    )


class TextGraphic(Graphic):
  def __init__(self, entity: Entity, style: Style = None, layer: int = MIDDLE_LAYER) -> None:
    if not style:
      style = default_text_style()

    super().__init__(entity, style, layer)
    self.layer = TOP_LAYER
    self.font = self.style.font

  def render(self) -> pygame.Surface:
    rendered: List[pygame.Surface] = []
    for text in self.text:
      rendered.append(self.font.render(text, False, WHITE).convert_alpha())

    width = max([r.get_width() for r in rendered])
    height = sum([r.get_height() for r in rendered])

    self.surface = pygame.Surface((width, height)).convert_alpha()
    self.surface.fill(TRANSPARENT)

    text_position = Vector(0, 0)
    for text_surface in rendered:
      self.surface.blit(text_surface, text_position.as_tuple())
      text_position += Vector(0, text_surface.get_height())

    return self.surface

  @property
  def text(self) -> List[str]:
    result: List[str] = [self.entity.name]
    if self.selected:
      result.append(str(self.entity.get_component(EnergyComponent)))
      desire_component: DesireComponent = self.entity.get_component(DesireComponent)
      if desire_component:
        result.append(str(desire_component.desire))
    
    return result

  def anchor(self) -> Vector:
    return Vector(0, self.surface.get_height()) / 2

  def scale(self, new_scale):
    pass

  def to_dict(self):
    return {
      'text': self.text
    }


class SpriteGraphic(Graphic):
  SPRITE_DIR = 'sprites'

  def __init__(self, entity: Entity, style: Style = Style(), layer: int = MIDDLE_LAYER, scale: float = 1.0):
    super().__init__(entity, style, layer)
    self._scale = self.original_scale = scale
    self.sprite_config: str | None = self.entity.properties.get('sprite', None)
    self.sprite_path: Path = self._get_sprite_file()

    if not self.sprite_path:
      raise FileNotFoundError(self.sprite_path)

    self.original_sprite = pygame.image.load(self.sprite_path).convert_alpha()
    self.surface = self.sprite = self.original_sprite

  def render(self) -> pygame.Surface:
    return self.sprite

  def scale(self, new_scale):
    if new_scale != self._scale:
      self._scale = new_scale
      ratio = self._scale / self.original_scale
      aspect_ratio = self.original_sprite.get_height() / self.original_sprite.get_width() * 1.0
      new_width = self.original_sprite.get_width() * ratio
      new_height = new_width * aspect_ratio
      size = (new_width, new_height)
      self.sprite = pygame.transform.scale(
        self.original_sprite,
        size
      )
      self.surface = self.sprite

  def _get_sprite_file(self) -> Path | None:
    if self._no_load():
      return None
    else:
      base_dir = SpriteGraphic.SPRITE_DIR
      if not self.sprite_config:
        return self._get_entity_name_file(base_dir)
      elif self.sprite_config.lower() == 'random':
        return random.choice(list(Path(base_dir).iterdir()))
      else:
        return self.get_direct_path(base_dir)

  def get_direct_path(self, base_dir):
    absolute_path = Path(self.sprite_config)
    relative_path = Path(f"{base_dir}/{self.sprite_config}")
    if absolute_path.exists():
      return absolute_path
    elif relative_path.exists():
      return relative_path
    else:
      return None

  def _get_entity_name_file(self, base_dir):
    name_path = Path(f"{base_dir}/{self.entity.name}.png")
    return name_path if name_path.exists() else None

  def _no_load(self):
    return self.sprite_config and self.sprite_config.lower() == 'no_load'


class VectorGraphic(Graphic):
  def __init__(self, entity: Entity, vector_func: Vector | Callable[[], Vector], style: Style = Style(), layer: int = MIDDLE_LAYER):
    super().__init__(entity, style=style, layer=layer)
    self._scale = 1.0
    self.surface = None
    self.vector_func = vector_func
    self.vector = self.vector_func() if isinstance(self.vector_func, Callable) else self.vector_func
    self.draw()

  def render(self) -> pygame.Surface:
    self.draw()
    return self.surface

  def scale(self, new_scale):
    if self._scale != 3 * new_scale:
      self._scale = 3 * new_scale
      self.surface = None

  def draw(self):
    self.vector = self.vector_func() if isinstance(self.vector_func, Callable) else self.vector_func
    scaled_vector = self.vector * self._scale
    surface_size = Vector(abs(scaled_vector.x), abs(scaled_vector.y))
    self.surface = pygame.Surface(surface_size.as_tuple()).convert_alpha()

    self.surface.fill(TRANSPARENT)

    start_x, end_x = (0, self.surface.get_width()) if self.vector.x > 0 else (self.surface.get_width(), 0)
    start_y, end_y = (0, self.surface.get_height()) if self.vector.y > 0 else (self.surface.get_height(), 0)

    # Main body
    pygame.draw.line(
      self.surface,
      self.style.color,
      (start_x, start_y),
      (end_x, end_y)
    )

    # End
    pygame.draw.circle(
      self.surface,
      pygame.Color(255,0,0),
      (end_x, end_y),
      self.style.border_width
    )

  def anchor(self) -> Vector:
    x = self.surface.get_width() if self.vector.x < 0 else 0
    y = self.surface.get_height() if self.vector.y < 0 else 0

    return Vector(x, y)
