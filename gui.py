import sys
from time import time
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
import traceback
from copy import deepcopy
from tkinter import filedialog, messagebox
from tkinter.filedialog import FileDialog
from typing import Any, Callable, Dict, List
import sv_ttk

import matplotlib
import matplotlib.pyplot as plt
import yaml
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from creatures.behavior import MoveRelative, MoveTo
from creatures.load import Loader, ParseException
from creatures.world import (Behavior, Entity, Frame, Location, Somewhere,
                             Vector, frame_generator)

DEFAULT_FILENAME = 'wander.yml'
PAUSE_TEXT = '⏸️'
PLAY_TEXT  = '▶️'

ACTIONS = {
  'move_up': {
    'action': MoveRelative(None, Vector(0, 10)),
    'label': '⬆',
    'position': (0, 1)
  },
  'move_down':  {
    'action': MoveRelative(None, Vector(0, -10)),
    'label': '⬇',
    'position': (2, 1)
  },
  'move_left':  {
    'action': MoveRelative(None, Vector(-10, 0)),
    'label': '⬅',
    'position': (1, 0)
  },
  'move_right': {
    'action': MoveRelative(None, Vector(10, 0)),
    'label': '➡',
    'position': (1, 2)
  },
}

DUMMY = Entity('dummy', Somewhere().get())

def current_time():
  return time() * 1000

class App(tkinter.Tk):
  def __init__(self, filename: str) -> None:
    super().__init__()
    self.title('opa')
    sv_ttk.set_theme('dark')
    self.paused = True
    self.tree_frame = None
    self.tree = None
    self.tree_values_by_uuid = {}
    self.anim = None
    self.animated = True
    self.chart = None
    self._current_frame = Frame(None)
    
    # Open() does not work as intended. Use cmdline args instead 
    # self._create_menu()
    self.control_panel = ControlPanel(self)
    self._load_frame(filename)

  def _load_frame(self, filename: str = DEFAULT_FILENAME):
    self.current_frame = Loader(filename).load()
    self.frames = frame_generator(self.current_frame)

    if self.chart:
      self.chart.get_tk_widget().destroy()

    self._create_plot_frame()
    self.title(filename)

  def _create_plot_frame(self):
    matplotlib.use('TkAgg')
    self.fig, self.ax = plt.subplots()
    self.chart = FigureCanvasTkAgg(self.fig, self)

    self.chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    if self.animated:
      self.anim = FuncAnimation(self.fig, self._animate, frames=self.frames, interval=20)
    else:
      self._animate()

  def _animate(self, frame: Frame = None):
    if frame:
      self.current_frame = frame
    self.ax.clear()
    self.ax.set_xlim([0, self.current_frame.world.width])
    self.ax.set_ylim([0, self.current_frame.world.height])
    self.ax.grid()
    for entity in self.current_frame.world.entities():
      self.ax.plot(
        entity.position.x,
        entity.position.y,
        marker="o",
        markersize=entity.properties.get('size', 5),
        markeredgecolor="black",
        markerfacecolor=entity.properties.get('color', 'green')
      )
      plt.annotate(entity.properties.get('name', entity.id), (entity.position._x + 2, entity.position._y))
    self.chart.draw()

  def behavior(self, behavior: Behavior):
    self.actor.behavior = behavior
    self.control_panel.update()
  
  def step(self):
    behavior = self.actor.behavior
    next_frame = Frame(deepcopy(self.current_frame.world))
    next_frame.world.update()
    self._animate(next_frame)
    self.actor.behavior = behavior
    self.control_panel.update()

  def toggle_pause(self, *args, **kwargs):
    if self.paused:
      self.anim.resume()
    else:
      self.anim.pause()

    self.paused = not self.paused
  
  def save(self):
    filename = filedialog.asksaveasfilename()
    if filename:
      with open(filename, 'w') as fd:
        yaml.dump(self.current_frame.to_dict(), stream=fd, allow_unicode=True, encoding=('utf-8'), sort_keys=False)
  
  def open(self):
    try:
      filename = filedialog.askopenfilename()
      self._load_frame(filename)
    except ParseException as pe:
      messagebox.showerror(title=str(pe.__class__.__name__), message=pe.msg)
    except Exception as e:
      traceback.print_exc(e)
      messagebox.showerror(title=str(e.__class__.__name__), message=f"Unexpected error: {str(e)}")
  
  @property
  def current_frame(self) -> Frame:
    return self._current_frame
  
  @property
  def actor(self) -> Entity:
    if self.current_frame.world:
      return self.current_frame.world.entities_map.get('agent', DUMMY)
    else:
      return DUMMY
  
  @property
  def target(self) -> Entity:
    if self.current_frame.world:
      return self.current_frame.world.entities_map.get('target', DUMMY)
    else:
      return DUMMY

  @current_frame.setter
  def current_frame(self, new_frame: Frame):
    self._current_frame = new_frame
    self.control_panel.update()

  def _create_menu(self):
    menubar = tk.Menu(self)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label="Open", command=self.open)
    filemenu.add_command(label="Save", command=self.save)
    filemenu.add_command(label="Exit", command=self.destroy)

    menubar.add_cascade(label="File", menu=filemenu)

    self.config(menu=menubar)

class ControlPanel(ttk.Frame):
  def __init__(self, master: App):
    super().__init__(master)
    self.master = master
    self.pack(side=tk.RIGHT)
    self.cards: List[Card] = []
    self.last_update = current_time()
    self._create_control_panel()
  
  def update(self) -> None:
    for card in self.cards:
      card.update()
    if self.master.animated:
      self.pause_button_label.set(PLAY_TEXT if self.master.paused else PAUSE_TEXT)
    self.last_update = current_time()
    super().update()

  def _create_control_panel(self):
    self.world_card = Card(self, 'world')
    self.world_card.add_row('Current Frame:', lambda: self.master.current_frame.number)
    self.world_card.add_row('Frame time: ', lambda: f"{current_time() - self.last_update:.2f}ms")
    self.world_card.pack()
    self.cards.append(self.world_card)

    self.actor_card = Card(self, 'actor')
    self.actor_card.add_row('Actor Name:', lambda: self.master.actor.properties.get('name', self.master.actor.id))
    self.actor_card.add_row('Actor position:', lambda: self.master.actor.position)
    self.actor_card.add_row('Actor current behavior:', lambda: str(self.master.actor.behavior if self.master.actor.behavior else None))
    self.actor_card.pack()
    self.cards.append(self.actor_card)
    if self.master.target:
      self.target_card = Card(self, 'target')
      self.target_card.add_row('Actor-Target Distance:', lambda: f"{(self.master.actor.distance(self.master.target)):.2f}")
      self.target_card.add_row('Target Name:', lambda: self.master.target.properties.get('name', self.master.actor.id))
      self.target_card.add_row('Target position:', lambda: self.master.target.position)
      self.target_card.add_row('Target current behavior:', lambda: str(self.master.target.behavior if self.master.target.behavior else None))
      self.target_card.pack()
      self.cards.append(self.target_card)

    if self.master.animated:
      self.pause_button_label = tk.StringVar(name='pause_button_label', value=PAUSE_TEXT)
      self.pause_button = ttk.Button(self, textvariable=self.pause_button_label, command=self.master.toggle_pause)
      self.pause_button.pack()
    else:
      btn_frame = ttk.Frame(self)
      for value in ACTIONS.values():
        btn = ttk.Button(btn_frame, text=value['label'], command=lambda a=value['action']: self.master.behavior(a))
        row, column = value['position']
        btn.grid(row=row, column=column)
      
      step_btn = ttk.Button(btn_frame, text='Step', command=self.master.step)
      step_btn.grid(row=1, column=3)
      
      btn_frame.grid(row=self.next_row_num, column=0)

class LabeledValue(object):
  def __init__(self, master: ControlPanel, label: str, initial_value: str, row: int, update_fn: Callable = None) -> None:
    self.master    = master
    self.label     = label
    self.value     = initial_value
    self.row       = row
    self.update_fn = update_fn
    
    self.tk_label  = ttk.Label(self.master, text=self.label)
    
    self.tk_var    = tkinter.StringVar(name=f"{self.label}_var", value=self.value)
    self.msg       = ttk.Label(self.master, textvariable=self.tk_var)
    
    self.tk_label.grid(row=self.row, column=0, sticky=tk.W)
    self.msg.grid(row=row, column=1, sticky=tk.E)
  
  def update(self):
    if self.update_fn:
      self.tk_var.set(self.update_fn())

class Card(ttk.Labelframe):
  def __init__(self, master, title: str, *args, **kwargs) -> None:
    super().__init__(master, text=title, *args, **kwargs)
    self.rows: List[LabeledValue] = []
  
  @property
  def next_row_num(self) -> int:
    return len(self.rows)
  
  def add_row(self, label: str, update_fn: Callable, initial_value: str = None):
    if not initial_value:
      initial_value = update_fn()
    row = LabeledValue(self, label, initial_value, self.next_row_num, update_fn)
    self.rows.append(row)
  
  def update(self) -> None:
    for row in self.rows:
      row.update()

if __name__ == '__main__':
  filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILENAME
  app = App(filename)
  app.mainloop()
  app.destroy()