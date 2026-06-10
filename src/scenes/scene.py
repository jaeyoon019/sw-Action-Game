from __future__ import annotations

import pygame


class Scene:
    def __init__(self, game: "Game") -> None:  # noqa: F821
        self.game = game

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass
