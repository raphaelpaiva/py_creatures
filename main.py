import sys
from time import time
import traceback

from core.action.action import ActionSystem
from core.brain.brain_system import BrainSystem
from core.creatures.creature import Creature
from core.desire import Wander
from core.desire.desire_system import DesireSystem
from core.energy import EnergySystem

from core.io.load import Loader, ParseException
from core.movement import MovementSystem
from core.render_system import RenderSystem
from core.sensor.sensor_system import SensorSystem
from core.world import World

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
    world.add_system(BrainSystem(world))
    world.add_system(SensorSystem())
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
    world.update()

def benchmark_loop(world):
  print('Benchmarking...')
  progress = 0
  for frame in range(BENCHMARK_FRAME_NUMBER):
    progress = 100 * frame / BENCHMARK_FRAME_NUMBER
    print(progress)
    
    world.update()

def time_ms():
    return time() / 1000 


if __name__ == '__main__':
  main()