from typing import List
from core.component.component import Component, EnergyComponent
from core.desire.desire_abstract import DesireComponent
from core.entity import Entity
from core.primitives import Vector
from core.render_system.constants import BORDER_WIDTH, NICE_COLOR


class SimpleGraphicComponent(Component):
  def __init__(self, entity: Entity) -> None:
    super().__init__()
    self.entity           = entity
    self.shape: str       = 'rect' if self.entity.is_resource else 'circle'
    self.color            = self.entity.properties.get('color', 'blue')
    self.size             = self.entity.properties.get('size', 5)
    self.border_width     = BORDER_WIDTH
    self.selected         = False
  
  def toggle_selected(self):
    self.selected = not self.selected

  @property
  def position(self) -> Vector:
    return self.entity.movement.position
  
  @property
  def text(self) -> List[str]:
    desire_component: DesireComponent = self.entity.get_component(DesireComponent)
    
    result: List[str] = []
    result.append(self.entity.name)
    if desire_component:
      result.append(str(desire_component.desire))
    result.append(str(self.entity.get_component(EnergyComponent)))
    
    return result