import pygame


class Checkpoint:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.activated = False

    def activate(self, player) -> None:
        if not self.activated:
            self.activated = True
            player.last_checkpoint = pygame.Vector2(self.rect.centerx, self.rect.bottom)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        color = (255, 220, 0) if self.activated else (160, 160, 160)
        draw_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, color, draw_rect)
