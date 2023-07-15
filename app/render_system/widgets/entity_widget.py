import pygame as pg
from typing import Dict
from textwrap import dedent
from core.component.component import EnergyComponent
from core.entity import Entity
from core.primitives import Vector
from app.desire import DesireComponent, MoveTo
from app.brain.brain_component import BrainComponent
from app.render_system.constants import ORIGIN
from .style import Style
from .text_widget import TextWidget
import app


class EntityWidget(TextWidget):
  def __init__(self, surface: pg.Surface, entity: Entity, position: Vector = ORIGIN, style: Style = Style()) -> None:
    self.entity = entity
    self.header = '--- Entity Widget ---\n'
    self.entity_text = f"{self.header}{self.dump()}"
    super().__init__(surface, self.entity_text, position=position, style=style)
  
  def update(self):
    self.entity_text = f"{self.header}{self.dump()}"
    self.set_text(self.entity_text)
    super().update()
  
  def dump(self) -> str:
    if self.entity:
      return dedent(
        f"""
        Id:{self._id()}
        Type: {self.entity.type}
        Move: {self._movement()}
        Desire:{self._desire()}
        Energy: {self._energy()}
        Brain: {self._brain()}
        """
      )
    else:
      return 'Select an entity'

  def _id(self):
    if self.entity.name and self.entity.name != self.entity.id:
      return f"{self.entity.name} | {self.entity.id}"
    else:
      return self.entity.id

  def _movement(self) -> str:
    movement = self.entity.movement
    if movement:
      return '|'.join([
        self._named_vector('P', movement.position),
        self._named_vector('V', movement.velocity),
        self._named_vector('A', movement.acceleration),
      ])
    else:
      return ''
  
  def _named_vector(self, name: str, vector: Vector) -> str:
    if name and vector:
      return f"{name}{self._vector(vector)}"
    else:
      return ''
  
  def _vector(self, vector: Vector) -> str:
    return f"({vector.x:.1f},{vector.y:.1f})" if vector != ORIGIN else '(O)'
  
  def _desire(self) -> str:
    desire_component: DesireComponent = self.entity.get_component(DesireComponent)
    if desire_component:
      match desire_component.desire.__class__:
        case app.desire.MoveTo:
          desire: MoveTo = desire_component.desire
          return f"MoveTo({desire.location})"
        case _:
          return desire_component.desire.__class__.__name__
    else:
      return ''
  
  def _energy(self) -> str:
    energy_component: EnergyComponent = self.entity.get_component(EnergyComponent)
    if energy_component:
      return f"{energy_component.current:.1f}/{energy_component.max_energy:.1f} - {energy_component.rate:.4f}"
    else:
      return ''

  def _brain(self) -> str:
    brain_component: BrainComponent = self.entity.get_component(BrainComponent)
    if brain_component:
      return f"""
          hunger thresh.: {brain_component.hunger_threshold}
          diet: {brain_component.diet_reasoner.__class__.__name__}
          {self._neurons()}
        """
    else:
      return ''

  def _neurons(self):
    brain_component: BrainComponent = self.entity.get_component(BrainComponent)
    if brain_component:
      neurons: Dict[str, float] = brain_component.input_neurons
      neurons_str = '\n  '.join([f"{k}: {v:.1f}" for k, v in neurons.items()])

      return f"""
neurons:
  {neurons_str}
"""
    return ''
