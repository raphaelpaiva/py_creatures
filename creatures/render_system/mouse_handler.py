import pygame as pg
from creatures.primitives import Vector

class Mouse(object):
  def __init__(self) -> None:
    self.is_down           = False
    self.is_up             = False
    self.left_pressed      = False
    self.right_pressed     = False
    self.relative_movement = Vector(0,0)
    self.position          = Vector(0,0)
  
  def update_position(self):
    self.relative_movement = Vector(*pg.mouse.get_rel())
    self.position          = Vector(*pg.mouse.get_pos())
  
  def update_button_state(
    self,
    is_down:           bool   = None,
    is_up:             bool   = None,
    left_pressed:      bool   = None,
    right_pressed:     bool   = None):

    self.is_down = is_down if is_down is not None else self.is_down
    self.is_up = is_up if is_up is not None else self.is_up
    self.left_pressed = left_pressed if left_pressed is not None else self.left_pressed
    self.right_pressed = right_pressed if right_pressed is not None else self.right_pressed
    