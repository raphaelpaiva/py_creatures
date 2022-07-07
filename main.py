import sys
import traceback

from creatures.load import Loader, ParseException
from creatures.world import frame_generator


DEFAULT_FILENAME = 'world.yaml'
DEFAULT_FRAME_NUMBER = 'infinite'

from plot import live_plot, generate_frames

def main():
  filename = DEFAULT_FILENAME
  frame_number = DEFAULT_FRAME_NUMBER
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  if len(sys.argv) > 2:
    frame_number = int(sys.argv[2])
  
  try:
    frame = Loader(filename).load()
    if frame_number == DEFAULT_FRAME_NUMBER:
      live_plot(frame_generator(frame))
    else:
      frames = generate_frames(frame_number, world=frame.world)
      live_plot(frames)
  except ParseException as e:
    print(e)
    exit(1)
  except Exception as e:
    traceback.print_exc() #sys.exc_info()[2]
    exit(255)

if __name__ == '__main__':
  main()