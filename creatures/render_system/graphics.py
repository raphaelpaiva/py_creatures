from typing import List
from creatures.component.component import Component, EnergyComponent
from creatures.entity import Entity
from creatures.primitives import Vector
from creatures.render_system.constants import BORDER_WIDTH, NICE_COLOR


class SimpleGraphicComponent(Component):
  def __init__(self, entity: Entity) -> None:
    super().__init__()
    self.entity           = entity
    self.shape: str       = 'rect' if self.entity.is_resource else 'circle'
    self.color            = self.entity.properties.get('color', 'blue')
    self.size             = self.entity.properties.get('size', 5)
    self.border_width     = BORDER_WIDTH
  
  @property
  def position(self) -> Vector:
    return self.entity.movement.position
  
  @property
  def text(self) -> List[str]:
    return [
      self.entity.name,
      str(self.entity.desire),
      str(self.entity.get_component(EnergyComponent.__name__))
    ]