import sys
from time import time
import logging
from typing import Dict, Callable, Self

from app.io import Loader, ParseException
from app.render_system import RenderSystem
from core.world import World
from app.creatures.creature import Creature

MODE_SIMULATION = 'simulation'
MODE_BENCHMARK = 'benchmark'

DEFAULT_FILENAME = 'scenarios/blue_creatures.yml'
DEFAULT_FRAME_NUMBER = 'infinite'
DEFAULT_MODE = MODE_SIMULATION
BENCHMARK_FRAME_NUMBER = 10000


class Application(object):
  BUILTIN_UIS: Dict[str | None, Callable[[World, Self], RenderSystem]] = {
    'gui_pygame': lambda w, a: RenderSystem(w, a),
    None: lambda w, a: None,
  }

  def __init__(self, filename: str, options: {}):
    super().__init__()
    self.log = logging.getLogger(Application.__name__)
    self.options = options
    self.filename: str = filename
    self.ui_type: str = 'gui_pygame' if not self.options.get('no_ui', False) else None

    self.world: World | None = None

    self.is_running = True
    self.dt = 0.0000001
    self.ui = None

  def load(self, random_seed=None):
    try:
      frame = Loader(self.filename, random_seed=random_seed).load()
      self.world: World = frame.world
    except ParseException as e:
      print(e)
      exit(1)

  def run(self):
    if self.is_benchmark:
      self.benchmark_loop()
      print()
      print(self.world.stats.get_dict())
    else:
      self.infinite_loop()

  def benchmark_loop(self):
    start = time()
    self.is_running = True
    print('Benchmarking...')
    for frame in range(BENCHMARK_FRAME_NUMBER):
      progress = 100 * frame / BENCHMARK_FRAME_NUMBER
      if progress and progress % 10 == 0:
        print('-', end='', flush=True)
      self.world.update()
    self.is_running = False
    print()
    print(f"{time() - start}s")

  def infinite_loop(self):
    logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s [%(levelname)s] %(filename)s:%(name)s.%(funcName)s(): %(message)s'
    )
    start = time_ms()
    self.ui = Application.BUILTIN_UIS[self.ui_type](self.world, self)
    dt = 0.000001
    while self.is_running:
      loop_start = time_ms()
      self.world.update(dt)
      if self.ui:
        self.ui.update(None)

      if not self.ui and not list(filter(lambda e: e.type == Creature.__name__, self.world.entities())):
        self.is_running = False
      dt = time_ms() - loop_start
    end = time_ms()
    self.log.info(f"Simulation clock: {self.world.clock / 1000}s (time res: {self.world.time_resolution}) |"
                  f" Wall clock: {(end - start) / 1000}s")

    if self.ui:
      self.ui.quit()

  def reset(self):
    self.load(random_seed=self.world.random_seed)

  def quit(self):
    self.is_running = False

  @property
  def is_benchmark(self) -> bool:
    return self.options.get('is_benchmark', False)


def main():
  log = logging.getLogger()
  filename = DEFAULT_FILENAME
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  options = {
    'is_benchmark': len(sys.argv) > 2 and '-b' in sys.argv,
    'no_ui': len(sys.argv) > 2 and '--no-ui' in sys.argv
  }

  try:
    app = Application(filename, options)
    app.load()
    app.run()
    sys.exit(0)
  except Exception as e:
    log.exception(e)
    exit(255)


def time_ms():
    return time() * 1000.0


if __name__ == '__main__':
  main()