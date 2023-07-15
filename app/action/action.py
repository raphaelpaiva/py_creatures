from typing import Any, Dict, List
from core.component import Component
from core.component.component import EnergyComponent
from core.entity import Entity
from core.primitives import Vector
from core.system import System

DEFAULT_MOVE_ACTION_ENERGY_COST: float = 0.01

class Action(object):
  def __init__(self) -> None: pass
  def run(self) -> None: pass
  @property
  def energy_cost(self): return 0.0
  def to_dict(self) -> Dict[str, Any]: pass


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
    return self._energy_cost * self.entity.properties.get('speed', 1.0)
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "self.direction": self.direction.to_dict(),
      "self._energy_cost": self._energy_cost
    }


class Grab(Action):
  def __init__(self, entity: Entity, target: Entity) -> None:
    super().__init__()
    self.entity = entity
    self.target = target
  
  def run(self) -> None:
    if self.target:
      energy_component = self.entity.get_component(EnergyComponent)
      energy_component.current = min(100, energy_component.current + 50)
      self.target.remove = True
  
  def to_dict(self) -> Dict[str, Any]:
    return {
      "target": self.target.id
    }


class ActionComponent(Component):
  def __init__(self) -> None:
    super().__init__()
    self.action: Action = None

  def to_dict(self) -> Dict[str, Any]:
    return {
      "action": self.action.to_dict() if self.action else None
    }


class ActionSystem(System):
  def __init__(self) -> None:
    super().__init__()
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      action_component: ActionComponent = entity.get_component(ActionComponent)
      energy_component: EnergyComponent = entity.get_component(EnergyComponent)

      if action_component and action_component.action:
        if energy_component:
          if energy_component.current >= action_component.action.energy_cost:
            action_component.action.run()
            energy_component.current -= action_component.action.energy_cost
          else:
            action_component.action = None
        else:
          action_component.action.run()
