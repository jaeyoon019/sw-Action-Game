import pygame

from scenes.menu import MenuScene
from scenes.scene import Scene
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.debug_font = pygame.font.SysFont(None, 24)
        self.running = True
        self.scene: Scene = MenuScene(self)

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)

            self.screen.fill((0, 0, 0))
            self.scene.draw(self.screen)
            self._draw_fps()
            pygame.display.flip()

        pygame.quit()

    def _draw_fps(self) -> None:
        text = f"FPS: {self.clock.get_fps():.0f}"
        surface = self.debug_font.render(text, True, (255, 255, 0))
        self.screen.blit(
            surface, (SCREEN_WIDTH - surface.get_width() - 10, 10)
        )


if __name__ == "__main__":
    Game().run()
