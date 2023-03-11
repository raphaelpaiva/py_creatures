from typing import List
import pygame as pg
from creatures.component import MovementComponent
from creatures.entity import Entity
from creatures.primitives import Vector

from creatures.render_system.aux_types import UIColor, UIPosition, UISize
from creatures.render_system.constants import BACKGROUND_GREY, BLACK, BORDER_WIDTH, DEFAULT_SIZE, GREEN, NICE_COLOR, ORIGIN
from creatures.render_system.widget import Widget
from creatures.world import World

class WorldWidget(Widget):
  def __init__(
    self,
    surface: pg.Surface,
    world: World,
    scale: float,
    font: pg.font.Font,
    position: UIPosition      = ORIGIN,
    size: UISize              = DEFAULT_SIZE,
    background_color: UIColor = BACKGROUND_GREY,
    border_width: int         = BORDER_WIDTH,
    border_color: UIColor     = BLACK,
    margin: int               = BORDER_WIDTH
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
  
  def update(self):
    sorted_entities = sorted(self.world.entities(), key=lambda e: e.size, reverse=True)
    self._render_bottom_layer(sorted_entities)
    self._render_middle_layer(sorted_entities)
    self._render_top_layer(sorted_entities)

  def _render_top_layer(self, sorted_entities: List[Entity]):
    for entity in sorted_entities:
      entity_border_width = 2 # TODO: Parametrize this
      size = entity.size * self.scale - entity_border_width
      
      entity_pos = entity.movement.position * self.scale + self.position
    
      text_offset = Vector(5 + size, -1 * size - 5)
      
      name_text = self.font.render(entity.properties.get('name', entity.id), True, NICE_COLOR)
      name_pos  = entity_pos + text_offset
      self.surface.blit(name_text, name_pos.as_tuple())

      behavior_text = self.font.render(str(entity.behavior), True, NICE_COLOR)
      behavior_pos  = name_pos + Vector(0, self.font.get_height())
      self.surface.blit(behavior_text, behavior_pos.as_tuple())

  def _render_middle_layer(self, sorted_entities: List[Entity]):
    for entity in sorted_entities:
      border_width = 2
      size = entity.size * self.scale - border_width
      
      entity_pos = entity.movement.position * self.scale + self.position
      
      if entity.is_resource:
        self._render_resource(entity, size, entity_pos)
      else:
        self._render_entity(entity, size, entity_pos)

  def _render_resource(self, entity: Entity, size: float, entity_pos: Vector):
    pg.draw.rect(
      self.surface,
      GREEN,
      pg.Rect(
        entity_pos.x - size / 2,
        entity_pos.y - size / 2,
        size,
        size,
      )
    )

    pg.draw.rect(
      self.surface,
      BLACK,
      pg.Rect(
        entity_pos.x - size / 2,
        entity_pos.y - size / 2,
        size,
        size,
      ),
      width=BORDER_WIDTH
    )
          
  def _render_entity(self, entity: Entity, size: float, entity_pos: Vector):
    pg.draw.circle(
      self.surface,
      entity.properties.get('color', NICE_COLOR),
      entity_pos.as_tuple(),
      size
    )
      
    pg.draw.circle(
      self.surface,
      BLACK,
      entity_pos.as_tuple(),
      size,
      width=BORDER_WIDTH
    )

  def _render_bottom_layer(self,sorted_entities: List[Entity]):
    for entity in sorted_entities:
      entity_pos = entity.movement.position * self.scale + self.position

      if 'sensor_radius' in entity.properties:
        pg.draw.circle(
        self.surface,
        BLACK,
        entity_pos.as_tuple(),
        entity.properties['sensor_radius'] * self.scale,
        width=BORDER_WIDTH
      )
