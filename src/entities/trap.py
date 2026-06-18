import pygame


class Trap:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)

    def collides_with(self, player_rect: pygame.Rect) -> bool:
        return self.rect.colliderect(player_rect)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        draw_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, (220, 50, 50), draw_rect)
