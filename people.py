import json
import sys
import yaml
from typing import List

from creatures.world import Frame, get_example_world

def main():
  w = get_example_world()

  frames = 10
  if len(sys.argv) > 1:
    frames = int(sys.argv[1])

  for frame in range(frames):
    frame = Frame(w)
    with open(f"frame_{frame.number}.yaml", 'w') as fd:
      yaml.dump(frame.to_dict(), stream=fd, allow_unicode=True, encoding=('utf-8'), sort_keys=False)
    with open(f"frame_{frame.number}.json", 'w') as fd:
      json.dump(frame.to_dict(), fd, indent=2)
    w.update()

if __name__ == '__main__':
  main()