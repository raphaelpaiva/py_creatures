from typing import List
from creatures.component import Component
from creatures.component.component import EnergyComponent
from creatures.entity import Entity, Vector
from creatures.system import System

DEFAULT_MOVE_ACTION_ENERGY_COST: float = 0.01

class Action(object):
  def __init__(self) -> None: pass
  def run() -> None: pass
  @property
  def energy_cost(self): return 0.0

class Move(Action):
  def __init__(self, entity: Entity, direction: Vector, energy_cost: float = DEFAULT_MOVE_ACTION_ENERGY_COST) -> None:
    super().__init__()
    self.entity = entity
    self.direction = direction
    self._energy_cost = energy_cost
  
  def run(self) -> None:
    old_velocity = self.entity.movement.velocity
    if old_velocity == Vector(0, 0):
      old_velocity = Vector(0,1) * self.entity.properties.get('speed', 1.0)
    self.entity.movement.velocity = self.direction.unit() * old_velocity.size()
  
  @property
  def energy_cost(self):
    return self._energy_cost

class Grab(Action):
  def __init__(self, entity: Entity, target: Entity) -> None:
    super().__init__()
    self.entity = entity
    self.target = target
  
  def run(self) -> None:
    if self.target.is_resource:
      energy_component = self.entity.get_component(EnergyComponent)
      energy_component.current = min(100, energy_component.current + 50)
      self.target.mark_remove = True


class ActionComponent(Component):
  def __init__(self) -> None:
    super().__init__()
    self.action: Action = None

class ActionSystem(System):
  def __init__(self) -> None:
    super().__init__()
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      action_component: ActionComponent = entity.get_component(ActionComponent.__name__)
      if action_component:
        action_component.action.run()
