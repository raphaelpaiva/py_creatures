from copy import deepcopy
import tkinter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import FileDialog
import tkinter.ttk as ttk
import traceback
from turtle import update
from types import NoneType
from typing import Any, Callable, Dict, List
import sv_ttk

import matplotlib
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yaml
from creatures.action import MoveRelative, MoveTo

from creatures.load import Loader, ParseException
from creatures.world import Action, Entity, Frame, Location, Vector, frame_generator

DEFAULT_FILENAME = 'training.yml'
PAUSE_TEXT = '⏸️'
PLAY_TEXT  = '▶️'

ACTIONS = {
  'move_up': {
    'action': MoveRelative(None, Vector(0, 10)),
    'label': '⬆'
  },
  'move_down':  {
    'action': MoveRelative(None, Vector(0, -10)),
    'label': '⬇'
  },
  'move_left':  {
    'action': MoveRelative(None, Vector(-10, 0)),
    'label': '⬅'
  },
  'move_right': {
    'action': MoveRelative(None, Vector(10, 0)),
    'label': '➡'
  },
}

class App(tkinter.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title('opa')
    sv_ttk.set_theme('dark')
    self.paused = True
    self.tree_frame = None
    self.tree = None
    self.tree_values_by_uuid = {}
    self.anim = None
    self.animated = False

    frames = self._load_frame()
    self._create_menu()
    self.control_panel = ControlPanel(self)

    self._create_plot_frame(frames)

  def _load_frame(self, filename: str = DEFAULT_FILENAME):
      frame = Loader(filename).load()
      frames = frame_generator(frame)

      self._current_frame = frame
      return frames

  def _create_plot_frame(self, frames):
      matplotlib.use('TkAgg')
      self.fig, self.ax = plt.subplots()
      self.chart = FigureCanvasTkAgg(self.fig, self)

      self.chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
      if self.animated:
        self.anim = FuncAnimation(self.fig, self._animate, frames=frames, interval=20)
      else:
        self._animate()

  def _animate(self, frame: Frame | NoneType = None):
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
  
  def _create_tree_view(self):
    if not self.tree_frame:
      self.tree_frame = ttk.Frame(self.control_panel_frame, padding="3")
      self.tree_frame.grid(row=0, column=0, sticky=tk.NSEW)
    
    self.tree = ttk.Treeview(self.tree_frame, columns='Values')
    self.tree.column('Values', width=100, anchor='center')
    self.tree.heading('Values', text='Values')

    self.tree.insert('', 'end', 'frame', text='Frame')
    self.tree.insert('frame', 'end', 'frame_number', text='number', values=self.current_frame.number)
    
    self.tree.insert('frame', 'end', 'world', text='World')
    self.tree.insert('world', 'end', 'world_width', text='width', values=self.current_frame.world.width)
    self.tree.insert('world', 'end', 'world_height', text='height', values=self.current_frame.world.height)
    self.tree.insert('world', 'end', 'world_entities', text='entities[]')

    for entity in self.current_frame.world.entities():
      iid = 'entity_' + entity.id
      title = entity.properties.get('name', entity.id)
      
      self.tree.insert('world_entities', 'end', iid, text=title)
      self.tree.insert(iid, 'end', f"{iid}_id", text='id', values=entity.id)
      self.tree.insert(iid, 'end', f"{iid}_location", text='location', values=entity.position)
      
      self.tree.insert(iid, 'end', f"{iid}_action", text='action')
      self._insert_tree_dict(f"{iid}_action", entity.action.to_dict())

    self.tree.item("frame", open=True)
    self.tree.item("world", open=True)
    self.tree.item("world_entities", open=True)
    #self.json_tree(self.tree, '', self.current_frame)
    
    
    self.tree.pack(fill=tk.BOTH, expand=1)

  def _insert_tree_dict(self, parent_iid: str, data: Dict[str, Any]):
    for key, value in data.items():
      iid = f"{parent_iid}_{key}"
      if isinstance(value, dict):
        self.tree.insert(parent_iid, 'end', iid, text=key)
        self._insert_tree_dict(iid, value)
      else:
        self.tree.insert(parent_iid, 'end', iid, text=key, values=value if value is not None else 'None')

  def _update_tree_dict(self, parent_iid: str, data: Dict[str, Any]):
    for key, value in data.items():
      iid = f"{parent_iid}_{key}"
      if isinstance(value, dict):
        self._update_tree_dict(iid, value)
      else:
        if value:
          self.tree.set(iid, 0, value)

  def action(self, action: Action):
    self.actor.action = action
    self.control_panel.update()
  
  def step(self):
    action = self.actor.action
    next_frame = Frame(deepcopy(self.current_frame.world))
    next_frame.world.update()
    self._animate(next_frame)
    self.actor.action = action
    self.control_panel.update()

  def toggle_pause(self, *args, **kwargs):
    if self.paused:
      self.anim.resume()
    else:
      self.anim.pause()
    
    self.paused = not self.paused
    self.pause_button_label.set(PLAY_TEXT if self.paused else PAUSE_TEXT)
  
  def save(self):
    filename = filedialog.asksaveasfilename()
    if filename:
      with open(filename, 'w') as fd:
        yaml.dump(self.current_frame.to_dict(), stream=fd, allow_unicode=True, encoding=('utf-8'), sort_keys=False)
  
  def open(self):
    try:
      filename = filedialog.askopenfilename()
      self._load_frame(filename)
      self._animate()
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
    return self.current_frame.world.entities_map['agent']
  
  @property
  def target(self) -> Entity:
    return self.current_frame.world.entities_map['target']

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

class ControlPanel(tk.Frame):
  def __init__(self, master: App):
    super().__init__(master)
    self.master = master
    self.pack(side=tk.RIGHT)
    self.rows: List[LabeledValue] = []
    self._create_control_panel()
  
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
    super().update()

  
  def _create_control_panel(self):
    self.add_row('Current Frame:', lambda: self.master.current_frame.number)
    self.add_row('Actor Name:', lambda: self.master.actor.properties.get('name', self.master.actor.id))
    self.add_row('Actor position:', lambda: self.master.actor.position)
    self.add_row('Actor current Action:', lambda: str(self.master.actor.action.to_dict() if self.master.actor.action else None))
    self.add_row('Actor-Target Distance:', lambda: str(self.master.actor.position.sub(self.master.target.position).size()))

    if self.master.animated:
      self.pause_button_label = tk.StringVar(name='pause_button_label', value=PAUSE_TEXT)
      self.pause_button = ttk.Button(self.control_panel_frame, textvariable=self.pause_button_label, command=self.toggle_pause)
      self.pause_button.grid(row=self.next_row_num, column=0, sticky=tk.N)
    else:
      btn_frame = ttk.Frame(self)
      for value in ACTIONS.values():
        btn = ttk.Button(btn_frame, text=value['label'], command=lambda a=value['action']: self.master.action(a))
        btn.pack(side=tk.LEFT)
      
      step_btn = ttk.Button(btn_frame, text='Step', command=self.master.step)
      step_btn.pack()
      
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

if __name__ == '__main__':
  app = App()
  app.mainloop()
  app.destroy()