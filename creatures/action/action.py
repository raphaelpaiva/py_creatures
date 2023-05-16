from typing import List
from creatures.component import Component
from creatures.entity import Entity, Vector
from creatures.system import System

class Action(object):
  def __init__(self) -> None: pass
  def run() -> None: pass

class Move(Action):
  def __init__(self, entity: Entity, direction: Vector) -> None:
    super().__init__()
    self.entity = entity
    self.direction = direction
  
  def run(self) -> None:
    old_velocity = self.entity.movement.velocity
    if old_velocity == Vector(0, 0):
      old_velocity = Vector(0,1) * self.entity.properties.get('speed', 1.0)
    self.entity.movement.velocity = self.direction.unit() * old_velocity.size()

class ActionComponent(Component):
  def __init__(self) -> None:
    super().__init__()
    self.action: Action = None

class ActionSystem(System):
  def __init__(self) -> None:
    super().__init__()
  
  def update(self, entities: List[Entity]):
    for entity in entities:
      actionComponents: List[ActionComponent] = entity.components.get(ActionComponent.__name__)
      if actionComponents:
        action = actionComponents[-1].action
        if action:
          action.run()
