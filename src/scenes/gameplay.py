from __future__ import annotations

from pathlib import Path

import pygame

from entities.player import Player
from scenes.scene import Scene
from settings import KEY_JUMP, SCREEN_HEIGHT, SCREEN_WIDTH
from systems.camera import Camera
from systems.stage import Stage


class GameplayScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        stage_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "tilemaps"
            / "mvp_stage.tmx"
        )
        self.stage = Stage(str(stage_path))
        self.player = Player(
            self.stage.spawn_point.x,
            self.stage.spawn_point.y,
        )
        self.camera = Camera()
        self.clear = False
        self.clear_font = pygame.font.SysFont(None, 72)
        self.prompt_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event: pygame.event.Event) -> None:
        if (
            self.clear
            and event.type == pygame.KEYDOWN
            and event.key == KEY_JUMP
        ):
            from scenes.menu import MenuScene

            self.game.change_scene(MenuScene(self.game))

    def update(self, dt: float) -> None:
        if self.clear:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt, self.stage.solids)
        self.camera.update(
            self.player.rect,
            self.stage.width,
            self.stage.height,
        )

        for trap in self.stage.traps:
            if trap.collides_with(self.player.rect):
                self.player.respawn()
                self.camera.update(
                    self.player.rect,
                    self.stage.width,
                    self.stage.height,
                )
                break

        for checkpoint in self.stage.checkpoints:
            if checkpoint.rect.colliderect(self.player.rect):
                checkpoint.activate(self.player)

        if self.stage.goal_rect.colliderect(self.player.rect):
            self.clear = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((35, 39, 47))
        self.stage.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        if self.clear:
            self._draw_clear_text(surface)

    def _draw_clear_text(self, surface: pygame.Surface) -> None:
        title = self.clear_font.render("STAGE CLEAR", True, (255, 255, 255))
        prompt = self.prompt_font.render(
            "Press Space to Menu",
            True,
            (220, 220, 220),
        )
        surface.blit(
            title,
            (
                SCREEN_WIDTH // 2 - title.get_width() // 2,
                SCREEN_HEIGHT // 2 - title.get_height(),
            ),
        )
        surface.blit(
            prompt,
            (
                SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                SCREEN_HEIGHT // 2 + 20,
            ),
        )
