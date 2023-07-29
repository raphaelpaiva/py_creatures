import sys
from time import time
import traceback
import logging

from app.action import ActionSystem
from app.brain.brain_system import BrainSystem
from app.desire import DesireSystem
from app.energy import EnergySystem

from app.io import Loader, ParseException
from core.movement import MovementSystem
from app.render_system import RenderSystem
from app.sensor.sensor_system import SensorSystem
from core.world import World
from app.creatures.creature import Creature

MODE_SIMULATION = 'simulation'
MODE_BENCHMARK = 'benchmark'

DEFAULT_FILENAME = 'scenarios/blue_creatures.yml'
DEFAULT_FRAME_NUMBER = 'infinite'
DEFAULT_MODE = MODE_SIMULATION
BENCHMARK_FRAME_NUMBER = 1000

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s [%(levelname)s] %(filename)s:%(name)s.%(funcName)s(): %(message)s'
)


class Application(object):
  def __init__(self, filename: str, mode: str = DEFAULT_MODE):
    super().__init__()
    self.log = logging.getLogger(Application.__name__)
    self.filename: str = filename
    self.mode: str = mode

    self.world: World | None = None

    self.is_running = True
    self.dt = 0.0000001
    self.ui = None

  def load(self, random_seed=None):
    try:
      frame = Loader(self.filename, random_seed=random_seed).load()
      self.world: World = frame.world
      self.world.add_system(BrainSystem(self.world))
      self.world.add_system(SensorSystem())
      self.world.add_system(DesireSystem())
      self.world.add_system(ActionSystem(self.world))
      self.world.add_system(MovementSystem(self.world))
      self.world.add_system(EnergySystem(self.world))

      #self.ui = RenderSystem(self.world, self)  # Load ui here
    except ParseException as e:
      print(e)
      exit(1)

  def run(self):
    if self.is_benchmark:
      self.benchmark_loop()
    else:
      self.infinite_loop()

  def benchmark_loop(self):
    self.is_running = True
    print('Benchmarking...')
    for frame in range(BENCHMARK_FRAME_NUMBER):
      progress = 100 * frame / BENCHMARK_FRAME_NUMBER
      print(progress)

      self.world.update()
    self.is_running = False

  def infinite_loop(self):
    start = time()
    self.world.time_resolution = 18
    dt = 0.000001
    while self.is_running:
      loop_start = time()
      self.world.update(dt)
      if self.ui:
        self.ui.update(None)

      if not self.ui and not list(filter(lambda e: e.type == Creature.__name__, self.world.entities())):
        self.is_running = False
      dt = time() - loop_start
    end = time()
    self.log.info(f"Simulation clock: {self.world.clock}s (time res: {self.world.time_resolution}) |"
                  f" Wall clock: {end - start}s")

    if self.ui:
      self.ui.quit()

  def reset(self):
    self.load(random_seed=self.world.random_seed)

  def quit(self):
    self.is_running = False

  @property
  def is_benchmark(self) -> bool:
    return self.mode is MODE_BENCHMARK


def main():
  log = logging.getLogger()
  filename = DEFAULT_FILENAME
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  is_benchmark = len(sys.argv) > 2 and sys.argv[2] == '-b'
  
  try:
    app = Application(filename, MODE_BENCHMARK if is_benchmark else DEFAULT_MODE)
    app.load()
    app.run()
    sys.exit(0)
  except Exception as e:
    log.exception(e)
    exit(255)


def time_ms():
    return time() / 1000.0


if __name__ == '__main__':
  main()