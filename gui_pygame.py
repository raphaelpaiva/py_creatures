import sys
from copy import deepcopy
import pygame as pg

from creatures.load import Loader
from creatures.world import Frame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
NICE_COLOR = (128, 11, 87)
WHITE = (255, 255, 255)

def main():
  print('loading frame')
  frame = Loader('movearound.yaml').load()

  print('initializing pygame')
  pg.init()

  screen = pg.display.set_mode( (SCREEN_WIDTH , SCREEN_HEIGHT) )
  scale = 0.8 * (SCREEN_WIDTH / frame.world.width)
  print(f"{scale=}")
  clock = pg.time.Clock()

  FPS = 0
  clock.tick(FPS)

  font = pg.font.SysFont(None, 24)
  name_text = font.render('hello', True, NICE_COLOR)

  while True:
    frametime = clock.tick(FPS) # In ms
    dt = frametime / 100
    fps = 1000 / (frametime + 0.00001)
    pg.display.set_caption(f"{fps=:03.2f} / {frametime}ms")
    handle_events()

    offset_x = 0.5 * (SCREEN_WIDTH - frame.world.width * scale)
    offset_y = 0.5 * (SCREEN_HEIGHT -  frame.world.height * scale)
    screen.fill(WHITE)
    pg.draw.rect(
      screen,
      (200, 200, 200),
      pg.rect.Rect(
        0 + offset_x,
        0 + offset_y,
        frame.world.width * scale,
        frame.world.height * scale
      )
    )
    for entity in sorted(frame.world.entities(), key=lambda e: e.size, reverse=True):
      border_width = 2
      size = entity.size * scale - border_width
      
      entity_pos = [
        entity.position.x * scale + offset_x,
        entity.position.y * scale + offset_y
      ]
      pg.draw.circle(
        screen,
        entity.properties.get('color', NICE_COLOR),
        entity_pos,
        size
      )
      pg.draw.circle(
        screen,
        (0, 0, 0),
        entity_pos,
        size,
        width=2
      )

      text_offset = [
        5 + size,
        -1 * size - 5
      ]
      name_text = font.render(entity.properties.get('name', entity.id), True, NICE_COLOR)
      name_pos  = [sum(x) for x in zip(entity_pos, text_offset)]
      screen.blit(name_text, name_pos)

      behavior_text = font.render(str(entity.behavior), True, NICE_COLOR)
      behavior_pos  = [sum(x) for x in (zip(name_pos, [0, behavior_text.get_height()]))]
      screen.blit(behavior_text, behavior_pos)
    
    frame = Frame(deepcopy(frame.world))
    frame.world.update(dt)
    pg.display.update()

def handle_events():
  for event in pg.event.get():
    if event.type == pg.QUIT:
      pg.quit()
      sys.exit()

if __name__ == '__main__':
  main()