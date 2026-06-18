from __future__ import annotations

import pygame

from settings import (
    DEATH_Y,
    GRAVITY,
    JUMP_VELOCITY,
    KEY_JUMP,
    KEY_LEFT,
    KEY_RIGHT,
    PLAYER_SPEED,
    TERMINAL_VELOCITY,
)


class Player:
    rect: pygame.Rect
    velocity: pygame.Vector2
    on_ground: bool
    last_checkpoint: pygame.Vector2

    def __init__(self, spawn_x: float, spawn_y: float) -> None:
        self.rect = pygame.Rect(int(spawn_x), int(spawn_y), 32, 32)
        self._position = pygame.Vector2(spawn_x, spawn_y)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.last_checkpoint = pygame.Vector2(spawn_x, spawn_y)

    def handle_input(self, keys) -> None:
        direction = int(keys[KEY_RIGHT]) - int(keys[KEY_LEFT])
        self.velocity.x = direction * PLAYER_SPEED

        if keys[KEY_JUMP] and self.on_ground:
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False

    def update(self, dt: float, solids: list[pygame.Rect]) -> None:
        self.velocity.y = min(
            self.velocity.y + GRAVITY * dt,
            TERMINAL_VELOCITY,
        )

        self._move_x(dt, solids)
        self._move_y(dt, solids)

        if self.rect.y > DEATH_Y:
            self.respawn()

    def draw(
        self,
        surface: pygame.Surface,
        camera_offset: pygame.Vector2,
    ) -> None:
        draw_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, (80, 200, 120), draw_rect)

    def respawn(self) -> None:
        self._position.update(self.last_checkpoint)
        self.rect.topleft = (
            round(self._position.x),
            round(self._position.y),
        )
        self.velocity.update(0, 0)
        self.on_ground = False

    def _move_x(self, dt: float, solids: list[pygame.Rect]) -> None:
        self._position.x += self.velocity.x * dt
        self.rect.x = round(self._position.x)

        for solid in solids:
            if not self.rect.colliderect(solid):
                continue

            if self.velocity.x > 0:
                self.rect.right = solid.left
            elif self.velocity.x < 0:
                self.rect.left = solid.right

            self._position.x = self.rect.x

    def _move_y(self, dt: float, solids: list[pygame.Rect]) -> None:
        self.on_ground = False
        self._position.y += self.velocity.y * dt
        self.rect.y = round(self._position.y)

        for solid in solids:
            if not self.rect.colliderect(solid):
                continue

            if self.velocity.y > 0:
                self.rect.bottom = solid.top
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = solid.bottom

            self.velocity.y = 0
            self._position.y = self.rect.y
