import sys
from time import time
import traceback

import pygame as pg
from creatures.behavior_system import BehaviorSystem

from creatures.load import Loader, ParseException
from creatures.render_system import RenderSystem

DEFAULT_FILENAME = 'scenarios/somecreatures.yml'
DEFAULT_FRAME_NUMBER = 'infinite'

def main():
  filename = DEFAULT_FILENAME
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  
  try:
    frame = Loader(filename).load()
    world = frame.world
    render_system = RenderSystem(world)
    world.add_system(render_system)
    world.add_system(BehaviorSystem())
    
    while True:
      handle_events()
      world.update()

  except ParseException as e:
    print(e)
    exit(1)
  except Exception as e:
    traceback.print_exc() #sys.exc_info()[2]
    exit(255)

def time_ms():
    return time() / 1000 

def handle_events():
  for event in pg.event.get():
    if event.type == pg.QUIT:
      pg.quit()
      sys.exit()

if __name__ == '__main__':
  main()