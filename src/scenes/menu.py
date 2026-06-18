import pygame

from scenes.gameplay import GameplayScene
from scenes.scene import Scene
from settings import KEY_JUMP, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


class MenuScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.title_font = pygame.font.SysFont(None, 72)
        self.prompt_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == KEY_JUMP:
            self.game.change_scene(GameplayScene(self.game))

    def draw(self, surface: pygame.Surface) -> None:
        title = self.title_font.render(TITLE, True, (255, 255, 255))
        prompt = self.prompt_font.render(
            "Press Space to Start", True, (200, 200, 200)
        )
        surface.blit(
            title,
            (
                SCREEN_WIDTH // 2 - title.get_width() // 2,
                SCREEN_HEIGHT // 3,
            ),
        )
        surface.blit(
            prompt,
            (
                SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                SCREEN_HEIGHT // 2,
            ),
        )
