import pygame as pg
from creatures.entity import Entity
from creatures.render_system.style import Style
from creatures.render_system.text_widget import TextWidget
import json

class EntityWidget(TextWidget):
  def __init__(self, surface: pg.Surface, entity: Entity, style: Style = ...) -> None:
    self.entity = entity
    self.entity_text = self.dump()
    super().__init__(surface, self.entity_text, style)
  
  def update(self):
    self.entity_text = self.dump()
    self.set_text(self.entity_text)
    super().update()
  
  def dump(self) -> str:
    return json.dumps(self.entity.to_dict(), indent=2, default=lambda o: '<Not Serializable>')
