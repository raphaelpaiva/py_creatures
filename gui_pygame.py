import sys
from copy import deepcopy
import pygame as pg

from creatures.load import Loader
from creatures.world import Frame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
NICE_COLOR = (128, 11, 87)
WHITE = (255, 255, 255)

print('loading frame')
frame = Loader('movearound.yaml').load()

print('initializing pygame')
pg.init()

SURFACE = pg.display.set_mode( (SCREEN_WIDTH , SCREEN_HEIGHT) )
SCALE = 0.8 * (SCREEN_WIDTH / frame.world.width)
print(f"{SCALE=}")
clock = pg.time.Clock()

FPS = 0
clock.tick(FPS)
while True:
  frametime = clock.tick(FPS) # In ms
  dt = frametime / 100
  fps = 1000 / (frametime + 0.00001)
  pg.display.set_caption(f"{fps=:03.2f} / {frametime}ms")
  for event in pg.event.get():
    if event.type == pg.QUIT:
      pg.quit()
      sys.exit()

  offset_x = 0.5 * (SCREEN_WIDTH - frame.world.width * SCALE)
  offset_y = 0.5 * (SCREEN_HEIGHT -  frame.world.height * SCALE)
  SURFACE.fill(WHITE)
  pg.draw.rect(
    SURFACE,
    (200, 200, 200),
    pg.rect.Rect(
      0 + offset_x,
      0 + offset_y,
      frame.world.width * SCALE,
      frame.world.height * SCALE
    )
  )
  for entity in sorted(frame.world.entities(), key=lambda e: e.properties.get('size', 2), reverse=True):
    size = entity.properties.get('size', 2) * SCALE
    position = (
      (entity.position.x * SCALE + offset_x),
      (entity.position.y * SCALE + offset_y)
    )
    pg.draw.circle(
      SURFACE,
      entity.properties.get('color', NICE_COLOR),
      position,
      size
    )
    pg.draw.circle(
      SURFACE,
      (0, 0, 0),
      position,
      size,
      width=2
    )

  frame = Frame(deepcopy(frame.world))
  frame.world.update(dt)
  pg.display.update()