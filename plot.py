from copy import deepcopy
import sys
from typing import List
from matplotlib.animation import FuncAnimation
import yaml
from people import World, Entity
from glob import glob
from matplotlib import pyplot as plt

from world import Frame, get_example_world

color_by_id = {
  'Zé': 'yellow',
  'Maria': 'red'
}

def prepare_plot():
  plt.rcParams["figure.figsize"] = [7.00, 3.50]
  plt.rcParams["figure.autolayout"] = True
  plt.xlim(0, 100)
  plt.ylim(0, 100)
  plt.grid()

def get_frames(param: str = None) -> List[Frame]:
  if isinstance(param, int):
    return generate_frames(param)
  else:
    return load_frames(param)

def load_frames(files) -> List[Frame]:
  frames = []
  for file in glob(files):
    with open(file, 'r') as fd:
      frame: Frame = yaml.load(fd, yaml.FullLoader)
      frames.append(frame)
  
  return frames

def generate_frames(number_of_frames: int, world: World = None) -> List[Frame]:
  frames = []
  world = world if world else get_example_world()
  for _ in range(number_of_frames):
    frames.append(Frame(deepcopy(world)))
    world.update()

  return frames

def plot(frame: Frame):
  for entity in frame.world.entities():
    plt.plot(entity.position._x, entity.position._y, marker="o", markersize=10, markeredgecolor="black", markerfacecolor=color_by_id.get(entity.id, 'green'))

def main():
  param = ''
  mode = 'live'
  if len(sys.argv) > 1:
    try:
      param = int(sys.argv[1])
    except:
      param = sys.argv[1]

  frames = get_frames(param)
  print(f"Frames: {len(frames)}")
  if mode == 'live':
    live_plot(frames)
  else:
    static_plot(frames)

def live_plot(frames: List[Frame]):
  fig, ax = plt.subplots()

  def animate(frame_number: int):
    frame = frames[frame_number]
    ax.clear()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    ax.grid()
    for entity in frame.world.entities():
      ax.plot(entity.position._x, entity.position._y, marker="o", markersize=10, markeredgecolor="black", markerfacecolor=color_by_id.get(entity.id, 'green'))
      plt.annotate(entity.id, (entity.position._x + 2, entity.position._y))

  ani = FuncAnimation(fig, animate, frames=len(frames), interval=30)
  plt.show()


def static_plot(frames: List[Frame]):
  prepare_plot()
  for frame in frames:
    plot(frame)

    entities: List[Entity] = frames[-1].world.entities()
    for entity in entities:
      plt.annotate(entity.id, (entity.position._x + 2, entity.position._y))
    plt.show()

if __name__ == '__main__':
  main()