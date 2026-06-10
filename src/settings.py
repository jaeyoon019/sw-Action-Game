import pygame

# 화면
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Action Game"

# 타일
TILE_SIZE = 16

# 물리 (단위: 픽셀, 초)
GRAVITY = 1200.0           # px/s^2
PLAYER_SPEED = 200.0       # px/s  (좌/우)
JUMP_VELOCITY = -500.0     # px/s  (음수 = 위)
TERMINAL_VELOCITY = 900.0  # px/s  (최대 낙하 속도)

# 사망 / 리스폰
DEATH_Y = 2000  # 플레이어 y가 이 값 초과 시 낙사

# 키 매핑
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_JUMP = pygame.K_SPACE
KEY_PAUSE = pygame.K_ESCAPE
