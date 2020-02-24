import enum

WINDOW_SIZE = (800, 800)
WINDOW_TITLE = 'SimEnv - Simple Evolution Simulation'
WINDOW_ICON_PATH = 'assets/icons/simenv.png'

FONT_PATH = 'assets/fonts/cascadia.ttf'

DEBUG_INFO_FONT_SIZE = 20


class HOVER_BY_CLASS_WEIGHT_ENUM(enum.IntEnum):
    GROUND_BLOCK = 0
    DIAN = 1
    
GROUND_BLOCK_SIZE = 32

class GROUND_BLOCK_TYPE_ENUM(enum.Enum):
    TOP_BLOCK = 1
    LEFT_BLOCK = 2
    RIGHT_BLOCK = 3
    BOTTOM_BLOCK = 4
    TOP_LEFT_BLOCK = 5
    TOP_RIGHT_BLOCK = 6
    BOTTOM_LEFT_BLOCK = 7
    BOTTOM_RIGHT_BLOCK = 8
    MIDDLE_BLOCK = 9


GROUND_POSITION_TO_TYPE = {
    (0, 0): GROUND_BLOCK_TYPE_ENUM.TOP_LEFT_BLOCK,
    (-1, 0): GROUND_BLOCK_TYPE_ENUM.TOP_RIGHT_BLOCK,
    (1, 0): GROUND_BLOCK_TYPE_ENUM.TOP_BLOCK,
    (0, -1): GROUND_BLOCK_TYPE_ENUM.BOTTOM_LEFT_BLOCK,
    (-1, -1): GROUND_BLOCK_TYPE_ENUM.BOTTOM_RIGHT_BLOCK,
    (0, 1): GROUND_BLOCK_TYPE_ENUM.LEFT_BLOCK,
    (-1, 1): GROUND_BLOCK_TYPE_ENUM.RIGHT_BLOCK,
    (1, -1): GROUND_BLOCK_TYPE_ENUM.BOTTOM_BLOCK,
    (1, 1): GROUND_BLOCK_TYPE_ENUM.MIDDLE_BLOCK,
}

GROUND_TYPE_TO_IMAGE_PATH = {
    GROUND_BLOCK_TYPE_ENUM.TOP_LEFT_BLOCK: 'assets/sprites/grass/topLeft.png',
    GROUND_BLOCK_TYPE_ENUM.TOP_RIGHT_BLOCK: 'assets/sprites/grass/topRight.png',
    GROUND_BLOCK_TYPE_ENUM.TOP_BLOCK: 'assets/sprites/grass/top.png',
    GROUND_BLOCK_TYPE_ENUM.BOTTOM_LEFT_BLOCK: 'assets/sprites/grass/bottomLeft.png',
    GROUND_BLOCK_TYPE_ENUM.BOTTOM_RIGHT_BLOCK: 'assets/sprites/grass/bottomRight.png',
    GROUND_BLOCK_TYPE_ENUM.LEFT_BLOCK: 'assets/sprites/grass/left.png',
    GROUND_BLOCK_TYPE_ENUM.RIGHT_BLOCK: 'assets/sprites/grass/right.png',
    GROUND_BLOCK_TYPE_ENUM.BOTTOM_BLOCK: 'assets/sprites/grass/bottom.png',
    GROUND_BLOCK_TYPE_ENUM.MIDDLE_BLOCK: 'assets/sprites/grass/middle.png',
}


FOOD_IMAGE_PATH = 'assets/sprites/food/localFauna.png'
MAX_STABLE_POPULATION_SIZE = 100

SPEED_FACTOR = 0.5

FPS_LIMIT = 60 * SPEED_FACTOR
TICKS_PER_DAY = 11
FRAMES_PER_TICK = 11
STARTING_POPULATATION_SIZE = 30

DIAN_IDLE_IMAGE_PATH = 'assets/sprites/dian/idle2.png'
DIAN_SLEEP_IMAGE_PATH = 'assets/sprites/dian/sleep2.png'
DIAN_MOVE_SPEED = 10 * SPEED_FACTOR
