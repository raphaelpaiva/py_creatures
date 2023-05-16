import sys
from time import time
import traceback

import pygame as pg
from creatures.action.action import ActionSystem
from creatures.desire.desire_system import DesireSystem
from creatures.energy import EnergySystem

from creatures.io.load import Loader, ParseException
from creatures.movement import MovementSystem
from creatures.render_system import RenderSystem
from creatures.world import World

DEFAULT_FILENAME = 'scenarios/somecreatures.yml'
DEFAULT_FRAME_NUMBER = 'infinite'
BENCHMARK_FRAME_NUMBER = 1000

def main():
  filename = DEFAULT_FILENAME
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  benchmark = len(sys.argv) > 2 and sys.argv[2] == '-b'
  
  try:
    frame = Loader(filename).load()
    world: World = frame.world
    world.add_system(DesireSystem())
    world.add_system(ActionSystem())
    world.add_system(MovementSystem(world))
    world.add_system(EnergySystem(world))
    world.add_system(RenderSystem(world))
    
    if benchmark:
      benchmark_loop(world)
    else:
      infinite_loop(world)

  except ParseException as e:
    print(e)
    exit(1)
  except Exception as e:
    traceback.print_exc() #sys.exc_info()[2]
    exit(255)

def infinite_loop(world: World):
  while True:
    handle_events()
    world.update()

def benchmark_loop(world):
  print('Benchmarking...')
  progress = 0
  for frame in range(BENCHMARK_FRAME_NUMBER):
    progress = 100 * frame / BENCHMARK_FRAME_NUMBER
    print(progress)
    
    handle_events()
    world.update()

def time_ms():
    return time() / 1000 

def handle_events():
  for event in pg.event.get():
    if event.type == pg.QUIT:
      pg.quit()
      sys.exit()

if __name__ == '__main__':
  main()