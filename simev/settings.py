import enum

WINDOW_SIZE = (800, 800)
WINDOW_TITLE = 'SimEnv - Simple Evolution Simulation'
WINDOW_ICON_PATH = 'assets/icons/simenv.png'

FONT_PATH = 'assets/fonts/cascadia.ttf'

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

GROUND_TYPE_TO_IMAGE = {
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

TICKS_PER_DAY = 11
FRAMES_PER_TICK = 30
