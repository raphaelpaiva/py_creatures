import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#ffffff'))

manager = pygame_gui.UIManager((800, 600))

window = pygame_gui.elements.UIWindow(
  rect=pygame.Rect((0, 0), (150, 150)),
  manager=manager,
  window_display_title='OPA',
  resizable=True
)

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                            text='Say Hello',
                                            manager=manager,
                                            container=window)



clock = pygame.time.Clock()
is_running = True

while is_running:
  time_delta = clock.tick(60)/1000.0
  pygame.draw.rect(background, pygame.Color('#000000'), pygame.Rect((400, 300), (50, 50)))
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          is_running = False
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == hello_button:
            print('Hello World!')

      manager.process_events(event)

  manager.update(time_delta)

  window_surface.blit(background, (0, 0))
  manager.draw_ui(window_surface)

  pygame.display.update()