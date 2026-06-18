import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Camera:
    def __init__(self) -> None:
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_rect: pygame.Rect, stage_width: int, stage_height: int) -> None:
        x = target_rect.centerx - SCREEN_WIDTH // 2
        y = target_rect.centery - SCREEN_HEIGHT // 2
        self.offset.x = max(0, min(x, stage_width - SCREEN_WIDTH))
        self.offset.y = max(0, min(y, stage_height - SCREEN_HEIGHT))
