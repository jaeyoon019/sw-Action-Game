from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import pygame

from entities.checkpoint import Checkpoint
from entities.trap import Trap


class Stage:
    solids: list[pygame.Rect]
    traps: list[Trap]
    checkpoints: list[Checkpoint]
    spawn_point: pygame.Vector2
    goal_rect: pygame.Rect
    width: int
    height: int

    def __init__(self, tmx_path: str) -> None:
        self.tmx_path = Path(tmx_path)
        self.solids = []
        self.traps = []
        self.checkpoints = []
        self.spawn_point = pygame.Vector2(0, 0)
        self.goal_rect = pygame.Rect(0, 0, 0, 0)
        self.width = 0
        self.height = 0
        self._tile_width = 16
        self._tile_height = 16
        self._loaded_with_pytmx = False
        self._tmx_data: Any | None = None

        self._load()

    def draw(
        self,
        surface: pygame.Surface,
        camera_offset: pygame.Vector2,
    ) -> None:
        if self._loaded_with_pytmx and self._tmx_data is not None:
            self._draw_tile_layers(surface, camera_offset)

        for rect in self.solids:
            self._draw_rect(surface, rect, camera_offset, (90, 90, 90))
        for trap in self.traps:
            trap.draw(surface, camera_offset)
        for checkpoint in self.checkpoints:
            checkpoint.draw(surface, camera_offset)
        if self.goal_rect.size != (0, 0):
            self._draw_rect(surface, self.goal_rect, camera_offset, (240, 210, 80))

    def _load(self) -> None:
        if not self.tmx_path.exists():
            raise FileNotFoundError(f"Stage file not found: {self.tmx_path}")

        try:
            self._load_with_pytmx()
        except ModuleNotFoundError:
            self._load_with_xml()

    def _load_with_pytmx(self) -> None:
        from pytmx import TiledObjectGroup, TiledTileLayer, load_pygame

        tmx_data = load_pygame(str(self.tmx_path))
        self._tmx_data = tmx_data
        self._loaded_with_pytmx = True
        self._tile_width = tmx_data.tilewidth
        self._tile_height = tmx_data.tileheight
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight

        for layer in tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer) and layer.name == "Solid":
                self._load_solid_tile_layer(layer)
            elif isinstance(layer, TiledObjectGroup):
                self._load_object_group(layer)

    def _load_with_xml(self) -> None:
        root = ET.parse(self.tmx_path).getroot()
        self._tile_width = int(root.attrib["tilewidth"])
        self._tile_height = int(root.attrib["tileheight"])
        self.width = int(root.attrib["width"]) * self._tile_width
        self.height = int(root.attrib["height"]) * self._tile_height

        for layer in root.findall("layer"):
            if layer.attrib.get("name") == "Solid":
                self._load_xml_solid_layer(layer)

        for object_group in root.findall("objectgroup"):
            self._load_xml_object_group(object_group)

    def _load_solid_tile_layer(self, layer: Any) -> None:
        for x, y, gid in layer:
            if gid == 0:
                continue
            self.solids.append(
                pygame.Rect(
                    x * self._tile_width,
                    y * self._tile_height,
                    self._tile_width,
                    self._tile_height,
                )
            )

    def _load_object_group(self, layer: Any) -> None:
        for obj in layer:
            rect = pygame.Rect(
                round(obj.x),
                round(obj.y),
                round(obj.width),
                round(obj.height),
            )
            self._assign_object(layer.name, rect)

    def _load_xml_solid_layer(self, layer: ET.Element) -> None:
        data = layer.find("data")
        if data is None or data.attrib.get("encoding") != "csv":
            return

        rows = csv.reader(data.text.strip().splitlines() if data.text else [])
        for y, row in enumerate(rows):
            for x, gid in enumerate(row):
                if int(gid.strip()) == 0:
                    continue
                self.solids.append(
                    pygame.Rect(
                        x * self._tile_width,
                        y * self._tile_height,
                        self._tile_width,
                        self._tile_height,
                    )
                )

    def _load_xml_object_group(self, object_group: ET.Element) -> None:
        layer_name = object_group.attrib.get("name", "")
        for obj in object_group.findall("object"):
            rect = pygame.Rect(
                round(float(obj.attrib.get("x", 0))),
                round(float(obj.attrib.get("y", 0))),
                round(float(obj.attrib.get("width", self._tile_width))),
                round(float(obj.attrib.get("height", self._tile_height))),
            )
            self._assign_object(layer_name, rect)

    def _assign_object(self, layer_name: str, rect: pygame.Rect) -> None:
        if layer_name == "Spawn":
            self.spawn_point.update(rect.topleft)
        elif layer_name == "Goal":
            self.goal_rect = rect
        elif layer_name == "Trap":
            self.traps.append(Trap(rect.x, rect.y, rect.width, rect.height))
        elif layer_name == "Checkpoint":
            self.checkpoints.append(
                Checkpoint(rect.x, rect.y, rect.width, rect.height)
            )
        elif layer_name == "Solid":
            self.solids.append(rect)

    def _draw_tile_layers(
        self,
        surface: pygame.Surface,
        camera_offset: pygame.Vector2,
    ) -> None:
        from pytmx import TiledTileLayer

        for layer in self._tmx_data.visible_layers:
            if not isinstance(layer, TiledTileLayer) or layer.name == "Solid":
                continue

            for x, y, image in layer.tiles():
                if image is None:
                    continue
                surface.blit(
                    image,
                    (
                        x * self._tile_width - camera_offset.x,
                        y * self._tile_height - camera_offset.y,
                    ),
                )

    def _draw_rect(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        camera_offset: pygame.Vector2,
        color: tuple[int, int, int],
    ) -> None:
        draw_rect = rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, color, draw_rect)
