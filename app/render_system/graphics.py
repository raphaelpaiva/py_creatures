import logging
from typing import Any, Dict, List

import pygame.image
from pathlib import Path
from core.random_generator import generator as random
from core.component.component import Component, EnergyComponent
from app.desire.desire_abstract import DesireComponent
from core.entity import Entity
from core.primitives import Vector
from app.render_system.constants import BLACK, BORDER_WIDTH, BOTTOM_LAYER, GREEN, MIDDLE_LAYER, TOP_LAYER
from app.sensor.sensor import RadialSensor
from app.sensor.sensor_component import SensorComponent


class SimpleGraphicComponent(Component):
  def __init__(self, entity: Entity) -> None:
    super().__init__()
    self.entity = entity
    self.graphics: List[Graphic] = [Graphic(self.entity)]
    self.selected = False
    sensor_component: SensorComponent = self.entity.get_component(SensorComponent)
    if sensor_component:
      for sensor in sensor_component.sensors:
        if isinstance(sensor, RadialSensor):
          self.graphics.append(Graphic(self.entity, size=int(sensor.radius), color='transparent', layer=BOTTOM_LAYER))
    if 'grab_radius' in self.entity.properties:
      graphic_size = self.entity.properties['grab_radius']
      self.graphics.append(
        Graphic(self.entity, size=graphic_size, color='transparent', border_color=GREEN, layer=BOTTOM_LAYER)
      )
  
    self.graphics.append(TextGraphic(self.entity))
  
  def toggle_selected(self):
    self.selected = not self.selected
    for graphic in self.graphics:
      graphic.selected = not graphic.selected
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      'entity': self.entity.id,
      'graphics': [g.to_dict() for g in self.graphics]
    }


class Graphic(object):
  def __init__(self, entity: Entity, shape: str = None, color: str = None, size: int = None, border_color: str = BLACK, border_width: int = BORDER_WIDTH, layer: int = MIDDLE_LAYER) -> None:
    self.entity = entity
    self.shape: str = shape if shape else ('rect' if self.entity.is_resource else 'circle')
    self.color = color if color else self.entity.properties.get('color', 'blue')
    self.size = size if size else self.entity.properties.get('size', 5)
    self.border_width = border_width
    self.border_color = border_color
    self.layer = layer
    
    self.selected = False
    self.original_sprite = self.sprite = load_sprite(self)
    self.converted = False
  
  @property
  def position(self) -> Vector:
    return self.entity.movement.position

  @property
  def graphics_component(self) -> SimpleGraphicComponent:
    return self.entity.get_component(SimpleGraphicComponent)

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


class TextGraphic(Graphic):
  def __init__(self, entity: Entity, shape: str = None, color: str = None, size: int = None, border_color: str = BLACK, border_width: int = BORDER_WIDTH, layer: int = MIDDLE_LAYER) -> None:
    super().__init__(entity, shape, color, size, border_color, border_width, layer)
    self.layer = TOP_LAYER

  @property
  def text(self) -> List[str]:
    result: List[str] = []
    result.append(self.entity.name)
    if self.selected:
      result.append(str(self.entity.get_component(EnergyComponent)))
      desire_component: DesireComponent = self.entity.get_component(DesireComponent)
      if desire_component:
        result.append(str(desire_component.desire))
    
    return result

  def to_dict(self):
    return {
      'text': self.text
    }


def load_sprite(graphic: Graphic) -> pygame.Surface | None:
  SPRITE_DIR = 'sprites'
  sprite_config : str | None = graphic.entity.properties.get('sprite', None)
  if sprite_config and sprite_config.lower() == 'no_load':
    return None
  else:
    if not sprite_config:
      sprite_config = f"{SPRITE_DIR}/{graphic.entity.name}.png"
      if Path(sprite_config).exists():
        return pygame.image.load(sprite_config)
    elif sprite_config.lower() == 'random':
      sprite_path = random.choice(list(Path(SPRITE_DIR).iterdir()))
      try:
        return pygame.image.load(sprite_path)
      except Exception as e:
        logging.getLogger('load_sprite').warning(f"Error loading {sprite_path}: {e}")
        return None
    else:
      if Path(sprite_config).exists():
        return pygame.image.load(sprite_config)
      elif Path(f"{SPRITE_DIR}/{sprite_config}").exists():
        return pygame.image.load(f"{SPRITE_DIR}/{sprite_config}")
      else:
        return None

