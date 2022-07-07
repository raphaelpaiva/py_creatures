import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from turtle import update
from typing import Any, Dict
import uuid
import sv_ttk

import matplotlib
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from creatures.load import Loader
from creatures.world import Frame, frame_generator

DEFAULT_FILENAME = 'movearound.yaml'
PAUSE_TEXT = '⏸️'
PLAY_TEXT  = '▶️'

class App(tkinter.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title('opa')
    sv_ttk.set_theme('dark')
    self.paused = False
    self.tree_frame = None
    self.tree = None
    self.tree_values_by_uuid = {}

    frames = self._load_frame()
    self._create_control_panel()
    
    self._create_plot_frame(frames)

  def _load_frame(self):
      filename = DEFAULT_FILENAME
      frame = Loader(filename).load()
      frames = frame_generator(frame)

      self._current_frame = frame
      return frames

  def _create_plot_frame(self, frames):
      matplotlib.use('TkAgg')
      self.fig, self.ax = plt.subplots()
      self.chart = FigureCanvasTkAgg(self.fig, self)

      self.chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
      self.anim = FuncAnimation(self.fig, self._animate, frames=frames, interval=20)

  def _create_control_panel(self):
      self.control_panel_frame = ttk.Frame(self)
      self.control_panel_frame.pack(side=tk.RIGHT)
      self.pause_button_label = tk.StringVar(name='pause_button_label', value=PAUSE_TEXT)
      self.pause_button = ttk.Button(self.control_panel_frame, textvariable=self.pause_button_label, command=self.toggle_pause)
      self.pause_button.grid(row=1, column=0, sticky=tk.N)

      self.current_frame_label = tkinter.StringVar(name='current_frame_label', value=self._current_frame.number)
      self.msg = ttk.Label(self.control_panel_frame, textvariable=self.current_frame_label)
      self.msg.grid(row=0, column=0, sticky=tk.N)

      self._create_tree_view()

  def _animate(self, frame: Frame):
    self.current_frame = frame
    self.ax.clear()
    self.ax.set_xlim([0, frame.world.width])
    self.ax.set_ylim([0, frame.world.height])
    self.ax.grid()
    for entity in frame.world.entities():
      self.ax.plot(
        entity.position.x,
        entity.position.y,
        marker="o",
        markersize=entity.properties.get('size', 5),
        markeredgecolor="black",
        markerfacecolor=entity.properties.get('color', 'green')
      )
      plt.annotate(entity.properties.get('name', entity.id), (entity.position._x + 2, entity.position._y))
  
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
        self._insert_tree_dict(iid, value)
      else:
        self.tree.insert(parent_iid, 'end', iid, text=key, values=value if value is not None else 'None')

  def _update_tree_dict(self, parent_iid: str, data: Dict[str, Any]):
    for key, value in data.items():
      iid = f"{parent_iid}_{key}"
      if isinstance(value, dict):
        self._update_tree_dict(iid, value)
      else:
        self.tree.set(f"{iid}_{key}", 0, value)

  def toggle_pause(self, *args, **kwargs):
    if self.paused:
      self.anim.resume()
    else:
      self.anim.pause()
    
    self.paused = not self.paused
    self.pause_button_label.set(PLAY_TEXT if self.paused else PAUSE_TEXT)
  
  @property
  def current_frame(self) -> Frame:
    return self._current_frame
  
  @current_frame.setter
  def current_frame(self, new_frame: Frame):
    self._current_frame = new_frame
    self.tree.set('frame_number', 0, self.current_frame.number)
    for entity in self.current_frame.world.entities():
      iid = f"{entity}_{entity.id}"
      self.tree.set(f"{iid}_location", 0, f"<{entity.position.x:.2f}, {entity.position.y:.2f}>")
      self._update_tree_dict(f"{iid}_action", entity.action.to_dict())

if __name__ == '__main__':
  app = App()
  app.mainloop()