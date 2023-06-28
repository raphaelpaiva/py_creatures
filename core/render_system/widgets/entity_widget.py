import pygame as pg
from core.entity import Entity
from core.primitives import Vector
from core.render_system.constants import ORIGIN
from .style import Style
from .text_widget import TextWidget
import json

class EntityWidget(TextWidget):
  def __init__(self, surface: pg.Surface, entity: Entity, position: Vector = ORIGIN, style: Style = Style()) -> None:
    self.entity = entity
    self.entity_text = f"Entity Widget\n---\n{self.dump()}"
    super().__init__(surface, self.entity_text, position=position, style=style)
  
  def update(self):
    self.entity_text = f"Entity Widget\n---\n{self.dump()}"
    self.set_text(self.entity_text)
    super().update()
  
  def dump(self) -> str:
    if self.entity:
      return json.dumps(self.entity.to_dict(), indent=2, default=lambda o: '<Not Serializable>')
    else:
      return 'Select an entity'
