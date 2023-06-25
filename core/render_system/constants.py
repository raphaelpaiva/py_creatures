from core.primitives import Vector
from core.render_system.aux_types import UIColor, UISize

TOP_LAYER     = 0
MIDDLE_LAYER  = 1
BOTTOM_LAYER  = 2

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = SCREEN_WIDTH
ZOOM_LEVEL    = 0.95
BORDER_WIDTH  = 2
WORLD_MARGIN  = 5
ORIGIN        = Vector(0, 0)
DEFAULT_SIZE  = UISize(SCREEN_WIDTH, SCREEN_HEIGHT)

FPS_LIMIT = 0

BACKGROUND_GREY = UIColor(200, 200, 200)
NICE_COLOR      = UIColor(128, 11, 87)
WHITE           = UIColor(255, 255, 255)
GREEN           = UIColor(10, 200, 10)
BLACK           = UIColor(0, 0, 0)