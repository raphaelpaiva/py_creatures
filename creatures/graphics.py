from creatures.component import Component
from creatures.render_system import BORDER_WIDTH, NICE_COLOR
from creatures.world import Entity, Vector

class SimpleGraphicComponent(Component):
  def __init__(self, entity: Entity) -> None:
    super().__init__(entity)
    self.position: Vector = self.entity.position
    self.shape: str       = 'rect' if self.entity.is_resource() else 'circle'
    self.color            = self.entity.properties.get('color', NICE_COLOR)
    self.size             = self.entity.size
    self.border_width     = BORDER_WIDTH
    